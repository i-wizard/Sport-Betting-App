from django.contrib import messages
from django.db.models import F
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, reverse, get_object_or_404
from django.utils import timezone
from django.views import View
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Wallet
from stack.models import Team
from trivia.forms import QuestionForm, ResultQuestionForm
from trivia.helpers.marking import Marking
from trivia.models import Question, Attempt


def index_view(request):
    questions = Question.objects.filter(status='open', closed_at__gt=timezone.now())
    num_entries = 0
    if request.user.is_authenticated:
        num_entries = Attempt.objects.filter(user=request.user.pk, question__status='open').count()
    return render(request, 'trivia/index.html', {'questions': questions, 'num_entries': num_entries})


class AdminTrivia(View):
    form = QuestionForm

    def get(self, request):
        questions = Question.objects.filter()
        teams = Team.objects.all().order_by('-id')
        return render(request, 'trivia/admin/index.html', {'questions': questions, 'form': self.form, 'teams': teams})

    # def post(self, request):
    #     form = self.form(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Question Added Successfully.')
    #         return HttpResponseRedirect(reverse('myadmin:trivia'))
    #
    #     questions = Question.objects.filter()
    #     teams = Team.objects.all().order_by('-id')
    #     return render(request, 'trivia/admin/index.html', {'questions': questions, 'form': form, 'teams': teams})


def cancel_question(request, pk):
    if request.method == 'POST':
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

        if not question.status == 'open':
            messages.warning(request, 'Question cannot be closed as status is not open.')
            return HttpResponseRedirect(reverse('myadmin:trivia'))

        if question.num_players > 0:
            attempts = Attempt.objects.filter(question=question.pk)

            for attempt in attempts:
                user_wallet = Wallet.objects.get(user=attempt.user.pk)
                user_wallet.balance = F('balance') + 20
                user_wallet.save(update_fields=('balance',))

        question.status = 'canceled'
        question.save(update_fields=('status',))

        messages.warning(request, 'Question canceled.')
        return HttpResponseRedirect(reverse('myadmin:trivia'))

    raise Http404


class AdminTriviaResult(View):
    form = ResultQuestionForm

    def get(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

        return render(request, 'trivia/admin/edit.html', {'question': question, 'form': self.form})

    def post(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

        if not question.status == 'open':
            messages.warning(request, 'Question cannot be resulted as status is not open.')
            return HttpResponseRedirect(reverse('myadmin:trivia_result', args=[pk]))

        form = self.form(request.POST, instance=question)

        if form.is_valid():
            question_instance = form.save()
            Marking(question_instance)
            messages.success(request, 'Question Resulted Successfully.')
            return HttpResponseRedirect(reverse('myadmin:trivia'))

        return render(request, 'trivia/admin/edit.html', {'question': question, 'form': self.form})


class QuestionView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        if question.closed_at <= timezone.now():
            messages.warning(request, 'Match is closed for entry.')
            return HttpResponseRedirect(reverse('trivia:index'))

        return render(request, 'trivia/details.html', {'question': question})

    def post(self, request, pk):
        team_a_score = request.POST.get('team_a_score')
        team_b_score = request.POST.get('team_b_score')
        total_corner_kicks = request.POST.get('total_corner_kicks')
        total_cards = request.POST.get('total_cards')

        if not team_a_score or not team_b_score or not total_corner_kicks or \
                not total_cards:
            messages.warning(request, 'Please fill in all fields.')
            return HttpResponseRedirect(reverse('trivia:question', args=[pk]))

        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

        if question.closed_at <= timezone.now():
            messages.warning(request, 'Match is closed for entry.')
            return HttpResponseRedirect(reverse('trivia:index'))

        wallet = Wallet.objects.get(user=request.user.pk)

        if wallet.balance < 20:
            messages.warning(request, 'Your balance is not enough. Please topup and try again.')
            return HttpResponseRedirect(reverse('trivia:question', args=[pk]))

        wallet.balance = F('balance') - 20
        wallet.save(update_fields=('balance',))

        Attempt.objects.create(user=request.user, question=question, team_a_score=team_a_score,
                               team_b_score=team_b_score, total_corner_kicks=total_corner_kicks, total_cards=total_cards)
        messages.success(request, 'Entry submitted Successfully.')
        return HttpResponseRedirect(reverse('trivia:index'))


class QuestionApiView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        closed_at = request.data.get('closed_at')
        event = request.data.get('event')
        team_a = request.data.get('team_a')
        team_b = request.data.get('team_b')
        team_a_logo = request.data.get('team_a_logo')
        team_b_logo = request.data.get('team_b_logo')

        if not closed_at or not event or not team_a or not team_b or not team_a_logo or not team_b_logo:
            return Response(data={'non_field_errors': 'Please complete all fields.'},
                            status=status.HTTP_400_BAD_REQUEST)

        Question.objects.create(closed_at=closed_at, event=event, team_a=team_a, team_b=team_b, team_a_logo=team_a_logo,
                                team_b_logo=team_b_logo)

        return Response(data=True, status=status.HTTP_200_OK)


def entries_view(request):
    entries = Attempt.objects.filter(user=request.user.pk)
    return render(request, 'trivia/entries.html', {'entries': entries})


def entry_view(request, pk):
    try:
        entry = Attempt.objects.get(pk=pk)
    except Attempt.DoesNotExist:
        raise Http404

    return render(request, 'trivia/entry.html', {'entry': entry})
