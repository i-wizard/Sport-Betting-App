from random import randint

from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils import timezone
from django.utils.decorators import decorator_from_middleware

from account.models import Wallet
from utilities.site_details import get_site_details
from core.models import Slider, GameSetting
from support.models import Support
from utilities.helper import Helper, Mailer
from .middleware import AdminCheckMiddleware
from users.models import User
from stack.models import Slip, ActiveGame, Team, Event, Match, Game, WeekEndRaffle, RafflePlayer
from django.views import View
from .forms import TeamCreationForm, EventCreationForm, ImageForm, AddUserForm, GamesSettingForm
from django.contrib import messages
from django.db.models import Sum

helper_func = Helper()


@decorator_from_middleware(AdminCheckMiddleware)
def dashboard(request):
    context = {
        'count_users': len(get_users_except_admin()),
        'bets': len(get_bets()),
        'games_count': len(get_games()),
        'wins': len(get_winners())
    }
    return render(request, 'site_admin/index.html', context)


def get_users_except_admin():
    return User.objects.filter(is_staff=False)


def get_bets():
    return Slip.objects.all()


def get_games():
    return ActiveGame.objects.all()


def get_winners():
    return Slip.objects.filter(game_fate=1)


class TeamsView(View):
    form = TeamCreationForm

    def get(self, request):
        self.form = self.form()
        queryset = Team.objects.all().order_by('-id')

        return render(request, 'site_admin/teams/index.html', {'teams': queryset, 'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        queryset = Team.objects.all().order_by('-id')

        if form.is_valid():
            form.save()
            messages.success(request, 'Team Added Successfully.')

        return render(request, 'site_admin/teams/index.html', {'teams': queryset, 'form': form})


def delete_team_view(request, pk):
    if request.method == 'POST':
        team = get_object_or_404(Team, pk=pk)
        team.delete()

        messages.success(request, 'Team deleted Successfully.')

    return HttpResponseRedirect(reverse('myadmin:teams'))


class EventsView(View):
    form = EventCreationForm

    def get(self, request):
        self.form = self.form()
        queryset = Event.objects.all().order_by('-id')
        return render(request, 'site_admin/events/index.html', {'events': queryset, 'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        queryset = Event.objects.all().order_by('-id')

        if form.is_valid():
            form.save()
            messages.success(request, 'Event Added Successfully.')

        return render(request, 'site_admin/events/index.html', {'events': queryset, 'form': form})


def delete_event_view(request, pk):
    if request.method == 'POST':
        e = get_object_or_404(Event, pk=pk)
        e.delete()

        messages.success(request, 'Event deleted Successfully.')

    return HttpResponseRedirect(reverse('myadmin:events'))


def games_view(request):
    games = ActiveGame.objects.all().order_by('-id')
    return render(request, 'site_admin/games/index.html', {'games': games})


def games_creation_view(request):
    return render(request, 'site_admin/games/create.html')


def game_matches_view(request, pk):
    try:
        game = ActiveGame.objects.get(pk=pk)
    except ActiveGame.DoesNotExist:
        raise Http404

    matches = Match.objects.filter(game_date=pk).order_by('role')

    return render(request, 'site_admin/games/matches.html', {'matches': matches, 'game': game})


def redirect_after_match_update(request, pk):
    messages.success(request, 'Match updated Successfully.')

    return HttpResponseRedirect(reverse('myadmin:game_matches', args=[pk]))


class ImagesView(View):
    form = ImageForm

    def get(self, request):
        form = self.form()
        queryset = Slider.objects.all().order_by('-id')
        return render(request, 'site_admin/images/index.html', {'images': queryset, 'form': form})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        queryset = Slider.objects.all().order_by('-id')

        if form.is_valid():
            form.save()
            messages.success(request, 'Image Added Successfully.')

        return render(request, 'site_admin/images/index.html', {'images': queryset, 'form': form})


def add_slider_image(request, pk):
    if request.method == 'POST':
        s = get_object_or_404(Slider, pk=pk)
        s.should_show = True
        s.save()

        messages.success(request, 'Image added to slider.')

    return HttpResponseRedirect(reverse('myadmin:images'))


def remove_slider_image(request, pk):
    if request.method == 'POST':
        s = get_object_or_404(Slider, pk=pk)
        s.should_show = False
        s.save()

        messages.success(request, 'Image removed from slider.')

    return HttpResponseRedirect(reverse('myadmin:images'))


class UsersView(View):
    form = AddUserForm

    def get(self, request):
        form = self.form()
        users = User.objects.filter(is_staff=False).order_by('-id')
        q = request.GET.get('q', None)

        if q:
            users = users.filter(username__iregex=q)

        for user in users:
            user.num_bets = Slip.objects.filter(user=user.pk).count()
            user.num_loses = Slip.objects.filter(user=user.pk, game_fate=2).count()
            user.num_wins = Slip.objects.filter(user=user.pk, game_fate=1).count()

            try:
                wallet_bonus = Wallet.objects.get(user=user.pk)
                user.wallet_bonus = wallet_bonus.bonus_balance
            except Wallet.DoesNotExist:
                user.wallet_bonus = 0

            money = Slip.objects.filter(user=user.pk, game_fate=1).aggregate(Sum('amount_won'))
            amount = 0

            if money['amount_won__sum'] is not None:
                amount = money['amount_won__sum']
            user.profit = amount

        return render(request, 'site_admin/users/index.html', {'users': users, 'form': form})

    def post(self, request):
        form = self.form(request.POST)
        users = User.objects.filter(is_staff=False).order_by('-id')

        for user in users:
            user.num_bets = Slip.objects.filter(user=user.pk).count()
            user.num_loses = Slip.objects.filter(user=user.pk, game_fate=2).count()
            user.num_wins = Slip.objects.filter(user=user.pk, game_fate=1).count()

            money = Slip.objects.filter(user=user.pk, game_fate=1).aggregate(Sum('amount_won'))
            amount = 0

            if money['amount_won__sum'] is not None:
                amount = money['amount_won__sum']
            user.profit = amount

        if form.is_valid():
            form.save()

            user = User.objects.get(phone=form.cleaned_data.get('phone'))

            img_url = 'http://{}/static/images/logos/teams/team-{}.png'.format(get_site_details.get_site_url(),
                                                                               randint(1, 19))
            image = helper_func.urls_image_upload(img_url)

            user.set_password(form.cleaned_data.get('password').lower())
            user.is_active = True
            user.profile_image.save(image[0], image[1], save=True)

            messages.success(request, 'User added Successfully.')

        return render(request, 'site_admin/users/index.html', {'users': users, 'form': form})


def delete_slider_image(request, pk):
    if request.method == 'POST':
        s = get_object_or_404(Slider, pk=pk)
        s.delete()

        messages.success(request, 'Image deleted successfully.')

    return HttpResponseRedirect(reverse('myadmin:images'))


def game_edit_view(request, pk):
    try:
        game = ActiveGame.objects.get(pk=pk)
    except ActiveGame.DoesNotExist:
        raise Http404

    return render(request, 'site_admin/games/edit.html', {'game_id': game.pk})


def game_delete_view(request, pk):
    try:
        game = ActiveGame.objects.get(pk=pk)
    except ActiveGame.DoesNotExist:
        raise Http404

    slips = Slip.objects.filter(today=game.pk)
    matches = Match.objects.filter(game_date=game.pk)

    if slips.exists():
        for slip in slips:
            games = Game.objects.filter(slip=slip.pk)
            games.delete()

        slips.delete()
    matches.delete()
    game.delete()

    messages.success(request, 'Game and all of its record deleted.')
    return HttpResponseRedirect(reverse('myadmin:games'))


class GamesSetting(View):
    form = GamesSettingForm

    def get(self, request):
        form = self.form()
        try:
            setting = GameSetting.objects.get()
        except GameSetting.DoesNotExist:
            raise Http404
        return render(request, 'site_admin/games/setting.html', {'setting': setting, 'form': form})

    def post(self, request):
        form = self.form(request.POST)
        try:
            setting = GameSetting.objects.get()
        except GameSetting.DoesNotExist:
            raise Http404

        if form.is_valid():
            setting.min_user_limit = int(form.cleaned_data.get('min_user_limit'))
            setting.num_smart_users = int(form.cleaned_data.get('num_smart_users'))
            setting.num_jackpot_winners = int(form.cleaned_data.get('num_jackpot_winners'))
            setting.save()

            messages.success(request, 'Game settings updated!')

        return render(request, 'site_admin/games/setting.html', {'setting': setting, 'form': form})


def user_games_view(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404

    slips = Slip.objects.filter(user=pk).order_by('-id')

    return render(request, 'site_admin/users/games.html', {'user': user, 'slips': slips})


def user_bet_slip(request, pk):
    try:
        slip = Slip.objects.get(pk=pk)
    except Slip.DoesNotExist:
        raise Http404

    logout(request)
    return redirect(f'/slip/{slip.slip_token}')


def change_user_status(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404

    user.is_active = not user.is_active
    user.save()

    messages.success(request, 'Account status updated!')
    return redirect(f'/admin/users')


def support_view(request):
    issues = Support.objects.all().order_by('-timestamp')

    return render(request, 'site_admin/support/index.html', {'issues': issues})


class SupportResponse(View):
    def post(self, request):
        message = request.POST['message']
        user_name = request.POST['name']
        user_email = request.POST['email']

        if not message or len(message) < 1:
            messages.warning(request, 'Please enter your message.')

            if not user_name or not user_email:
                messages.warning(request, 'Request could not be validated please reload and try again.')

        mailer = Mailer()
        mailer.admin_response(message, user_email, user_name)
        messages.success(request, 'Message Sent!')

        return redirect(f'/admin/support')


class SendMessage(View):
    def get(self, request):
        users = User.objects.filter(is_staff=False, is_moderator=False, is_active=True).order_by('-id')
        q = request.GET.get('q', None)

        if q:
            users = users.filter(username__iregex=q)

        return render(request, 'site_admin/message/index.html', {'users': users})

    def post(self, request):
        users = User.objects.filter(is_staff=False, is_moderator=False, is_active=True).order_by('-id')
        emails = request.POST.getlist('emails')

        if not len(emails):
            messages.warning(request, 'Please select at least one email address')

        else:
            message = request.POST['message']
            title = request.POST['message_title']

            if len(message) and len(title):
                for email in emails:
                    mailer = Mailer()
                    mailer.admin_message(message, email, title)
                messages.success(request, 'Message Sent!')
            else:
                messages.warning(request, 'Please select at least one email address')
        return render(request, 'site_admin/message/index.html', {'users': users})


class CreditUserAccount(View):
    def get(self, request):
        return redirect('/admin/users')

    def post(self, request):
        amount = request.POST['bonus_balance']
        user_id = request.POST['user_id']

        if amount:
            try:
                amount = float(amount)
                try:
                    wallet = Wallet.objects.get(user=user_id)
                    wallet.bonus_balance = amount
                    wallet.save()

                    messages.success(request, 'Account credited!')
                except User.DoesNotExist:
                    messages.warning(request, 'Please enter amount')

            except ValueError:
                messages.warning(request, 'Please enter amount')
        else:
            messages.warning(request, 'Please enter amount')

        return redirect('/admin/users')


class QualifiedPlayers(View):
    def get(self, request):
        try:
            raffle = WeekEndRaffle.objects.get(is_active=True)
            players = RafflePlayer.objects.filter(raffle=raffle.pk)
        except WeekEndRaffle.DoesNotExist:
            players = []

        return render(request, 'site_admin/qualified_players.html', {'players': players})
