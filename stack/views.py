




from random import randint

from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import dateparse, timezone
from django.views import View
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import timedelta

from core.models import GameSetting
from referral.models import Referral
from stack.stock_helpers import StockHelper
from users.models import User
from utilities.raffle_id import RaffleIdGenerator
from utilities.slip_token import SlipTokenGenerator
from stack.models import Event, ActiveGame, Match, Slip, Game, Team, RafflePlayer, RaffleWinners, WeekEndRaffle
from account.models import Wallet
from utilities.helper import LargeResultsSetPagination, Mailer
from .stackSerializers import EventSerializer, GamesSerializer, MatchSerializer, UserGamesSerializer, \
    SlipGamesSerializer, TeamSerializer, SlipSerializer, RaffleWinnersSerializer, RafflePlayerSerializer
from utilities.helper import Helper

helpers = Helper()


class EventsApiView(generics.ListAPIView):
    queryset = Event.objects.all().order_by('-id')
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = EventSerializer
    pagination_class = LargeResultsSetPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.data, status=201)

    def delete(self, request):
        event = Event.objects.get(pk=request.data.get('event'))

        event.delete()

        return Response(status=status.HTTP_200_OK)


class CreationDataAPi(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_classes = (EventSerializer, TeamSerializer)

    def get(self, request):
        queryset = Event.objects.all().order_by('-id')
        queryset2 = Team.objects.all().order_by('-id')
        event_serializer = self.serializer_classes[0](queryset, many=True)
        team_serializer = self.serializer_classes[1](queryset2, many=True)

        return Response(data={'events': event_serializer.data, 'teams': team_serializer.data},
                        status=status.HTTP_200_OK)


class CreateGameApi(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        match_schedule_date = dateparse.parse_datetime(request.data.get('match_schedule_start_time')).date()

        matches = request.data.get('matches')
        if len(matches) < 10:
            return Response(data={'non_field_errors': 'You cannot make less than 10 selections.'},
                            status=status.HTTP_400_BAD_REQUEST)

        for match in matches:
            match.update(match_start_time=dateparse.parse_datetime(match.get('match_start_time')),
                         over_two_five=round(float(match.get('ov_twofive')), 2),
                         under_two_five=round(float(match.get('un_twofive')), 2),
                         home_team_odd=round(float(match.get('home_team_odd')), 2),
                         away_team_odd=round(float(match.get('away_team_odd')), 2),
                         even_odd=round(float(match.get('even_odd')), 2))

        match_schedule_start_time = matches[0]['match_start_time']

        if match_schedule_date < timezone.now().date():
            return Response(data={'non_field_errors': 'Please enter accurate game schedule time.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            ActiveGame.objects.get(schedule_date=match_schedule_date)

            return Response(data={'non_field_errors': 'A game is already scheduled for this date.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except ActiveGame.DoesNotExist:
            amount = 40000
            amount_available = 40000
            game_setting = GameSetting.objects.filter()[0]

            if game_setting:
                if timezone.now().date() <= game_setting.trial_ending:
                    amount = 20000
                    amount_available = 20000

            game = ActiveGame.objects.create(schedule_start_time=match_schedule_start_time,
                                             schedule_date=match_schedule_date, amount=amount,
                                             amount_available=amount_available)

            for match in matches:
                event = Event.objects.get(pk=match['event'])
                home_team = Team.objects.get(pk=match['home_team'])
                away_team = Team.objects.get(pk=match['away_team'])
                Match.objects.create(event=event, game_date=game, over_two_five=match['ov_twofive'],
                                     under_two_five=match['un_twofive'], home_team=home_team.name,
                                     away_team=away_team.name, home_team_odd=match['home_team_odd'],
                                     away_team_odd=match['away_team_odd'], even_odd=match['even_odd'],
                                     match_start_time=match['match_start_time'],
                                     role=match['role'])

            return Response(data=True, status=status.HTTP_200_OK)


class GamesView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GamesSerializer

    def get(self, request, date):
        try:
            if date == 1:
                game_date = timezone.now() + timezone.timedelta(days=1)
                game_date = game_date.date()
            else:
                game_date = timezone.now().date()

            game = ActiveGame.objects.get(schedule_date=game_date)
        except ActiveGame.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        match_queryset = Match.objects.filter(game_date=game.pk).prefetch_related('event').order_by('role')

        serializer = self.serializer_class(match_queryset, many=True)

        return Response(data={'matches': serializer.data, 'is_active': game.is_active,
                              'game_start_time': game.schedule_start_time},
                        status=status.HTTP_200_OK)


class PlayTodayGames(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        game_amount = request.data.get('games_amount')

        selected_matches = request.data.get('games')

        try:
            game_check = ActiveGame.objects.get(pk=selected_matches[0]['game_date'])
        except (ActiveGame.DoesNotExist, TypeError):
            return Response(data={'response': 'Request could not be completed at this time.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if game_check.is_active:
            return Response(data={'response': 'Game already in session.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            wallet = Wallet.objects.get(user=request.user.pk)
        except Wallet.DoesNotExist:
            return Response(data={'response': 'Request could not be completed at this time.'},
                            status=status.HTTP_400_BAD_REQUEST)

        balance_amount = wallet.balance
        bonus_enough = False

        if int(request.data.get('use_bonus')) == 1:
            if wallet.bonus_balance < game_amount:
                balance_amount = wallet.bonus_balance + wallet.balance
            else:
                bonus_enough = True
                balance_amount = wallet.bonus_balance

        if balance_amount >= game_amount:
            # one_match_record = Match.objects.get(pk=selected_matches[0]['id'])
            # game_self = ActiveGame.objects.get(pk=one_match_record.game_date.pk)
            slip_token = SlipTokenGenerator().token
            time = timezone.now()
            new_slip = Slip.objects.create(today=game_check, user=request.user, stake=game_amount,
                                           played_at=time,
                                           slip_token=slip_token)

            if int(request.data.get('use_bonus')) is 0:
                wallet.balance = F('balance') - game_amount
            else:
                if bonus_enough:
                    wallet.bonus_balance = F('bonus_balance') - game_amount
                else:
                    neg_sum = wallet.bonus_balance - game_amount
                    amount_left = game_amount + neg_sum

                    if amount_left == 0:
                        amount_left = -(neg_sum)

                    wallet.bonus_balance = 0
                    wallet.balance = F('balance') - amount_left
            wallet.save()

            if request.user.referred:
                referral = Referral.objects.get(user=request.user.pk)
                if not referral.is_settled:
                    referral.is_settled = True
                    referral.save(update_fields=('is_settled',))

                    referrer_wallet = Wallet.objects.get(user=referral.referrer.pk)
                    referrer_wallet.bonus_balance = F('bonus_balance') + 100
                    referrer_wallet.save(update_fields=('bonus_balance',))

                    mailing = Mailer()
                    mailing.send_referrer_winner(referral.referrer, request.user.username)

            for match in selected_matches:
                match_record = Match.objects.get(pk=match['id'], role=match['role'])

                Game.objects.create(slip=new_slip, match=match_record, home_team_win=match['home_team_selected'],
                                    away_team_win=match['away_team_selected'], both_even=match['even_selected'],
                                    under_two_five=match['under_two_five_selected'],
                                    over_two_five=match['over_two_five_selected'])

        else:
            return Response(data={
                'response': 'You do not have enough fund for your selection. Please fund your account and continue.'},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(data={},
                        status=status.HTTP_200_OK)


class TodayMatches(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializers_class = MatchSerializer

    def get(self, request):
        try:
            today_game = ActiveGame.objects.get(schedule_date=timezone.now().date())
        except ActiveGame.DoesNotExist:
            return Response(data={'response': 'There is no available match for today.'},
                            status=status.HTTP_400_BAD_REQUEST)

        matches = Match.objects.filter(game_date=today_game.pk).order_by('role')

        serializer = self.serializers_class(matches, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserGamesView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserGamesSerializer

    def get(self, request):
        query = request.GET.get('q')
        # print(query)
        if query == 'previous':
            # print("HEY")
            p7 = timezone.now() - timedelta(days=7)
            td = timezone.now()
            queryset = Slip.objects.filter(user=request.user.pk,
                                           played_at__range=(p7, td)).order_by('-played_at')
        else:
            queryset = Slip.objects.filter(user=request.user.pk, today__schedule_date=timezone.now().date()).order_by(
                '-played_at')

        serializer = self.serializer_class(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SlipGamesView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SlipGamesSerializer

    def get(self, token):
        try:
            token = int(token)
        except ValueError:
            return Response(data={'response': 'Invalid slip token.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            slip = Slip.objects.get(slip_token=token)
        except Slip.DoesNotExist:
            return Response(data={'response': 'Invalid slip token.'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Game.objects.filter(slip=slip.pk).order_by('id')

        serializer = self.serializer_class(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GameMatches(APIView):
    serializer_class = MatchSerializer

    def get(self, request, pk):
        try:
            game = ActiveGame.objects.get(pk=pk)
        except ActiveGame.DoesNotExist:
            return Response(data={'response': 'Request not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Match.objects.filter(game_date=game.pk).order_by('role')

        serializer = self.serializer_class(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        try:
            match = Match.objects.get(pk=request.data.get('id'), game_date=pk)
        except Match.DoesNotExist:
            return Response(data={'response': 'Request could not be validated.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if match.resulted is True:
            return Response(data={'response': 'This match has already been resulted.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            match.home_team_score = int(request.data.get('home_team_score', 0))
            match.away_team_score = int(request.data.get('away_team_score', 0))
            match.save()
        except ValueError:
            return Response(data={'response': 'Please enter a valid score.'},
                            status=status.HTTP_400_BAD_REQUEST)

        both_teams_score = int(match.home_team_score) + int(match.away_team_score)

        games = Game.objects.filter(match=match.pk, checked=False)

        if games.count():
            for game in games:
                game_data = Game.objects.get(pk=game.pk)

                game_slip = Slip.objects.get(pk=game_data.slip.pk)

                game_win = False
                score = 0

                if int(match.home_team_score) == int(match.away_team_score):
                    if game_data.both_even:
                        score += 3
                        game_win = True
                elif int(match.home_team_score) > int(match.away_team_score):
                    if game_data.home_team_win:
                        score += 3
                        game_win = True
                elif int(match.home_team_score) < int(match.away_team_score):
                    if game_data.away_team_win:
                        score += 3
                        game_win = True

                if game_data.under_two_five:
                    if both_teams_score < 3:
                        score += 1
                elif game_data.over_two_five:
                    if both_teams_score >= 3:
                        score += 1

                game_data.win = game_win
                game_data.checked = True
                game_data.points = score
                game_data.save(update_fields=('win', 'checked', 'points',))

                game_slip.score = F('score') + score
                game_slip.save(update_fields=('score',))

            stock_helper = StockHelper()
            stock_helper.play_smart_users(match)

        # print("HEY SKIPPED")
        match.resulted = True
        match.save()

        return Response(data=True, status=status.HTTP_200_OK)


def mybets_view(request):
    today = timezone.now()
    day_tosix = today.weekday() + 6  # add 6 to day of the week
    date_difference = day_tosix - 5  # minus by 5 to get sunday's day
    sunday_date = timezone.now() - timezone.timedelta(days=date_difference)  # get the most recent sundays date
    sunday_date = timezone.make_aware(
        timezone.datetime(sunday_date.year, sunday_date.month, sunday_date.day, 20, 5, 0, 0))
    num_bets = Slip.objects.filter(jackpot_check=False, user=request.user.pk, played_at__gte=sunday_date).count()
    remaining_bets = 5 - num_bets
    raffle_id = ''
    if num_bets >= 5:
        try:
            raffle_id = RafflePlayer.objects.get(user=request.user.pk, raffle__ended=False).raffle_hash
        except RafflePlayer.DoesNotExist:
            raffle_id = ''
    return render(request, 'bets/mybets.html',
                  {'num_bets': num_bets, 'raffle_id': raffle_id, 'remaining_bets': remaining_bets})


class BetSlips(APIView):
    serializer_class = SlipSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', timezone.now().date())
        q_filter = request.GET.get('filter', 0)
        queryset = Slip.objects.filter(user=request.user.pk).order_by('-id')

        if not q == 'Filter by day' and not q == '':
            queryset = queryset.filter(played_at__date=q)

        if int(q_filter) is 0:
            queryset = queryset.filter(game_fate=0)
        else:
            queryset = queryset.filter(game_fate__gte=1)

        serializer = self.serializer_class(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


def slip_details_view(request, token):
    slip = get_object_or_404(Slip, slip_token=token.lower())

    return render(request, 'bets/slip.html', {'slip': slip})


def slip_details_q_view(request):
    q = request.GET.get('q', '')

    slip = get_object_or_404(Slip, slip_token=q.lower())

    return render(request, 'bets/slip.html', {'slip': slip})


def winners_list(request):
    return render(request, 'bets/winners.html')


def jackpot_winners_list(request):
    return render(request, 'bets/raffle_winners.html')


class WinnersChart(APIView):
    serializer_class = SlipSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        if len(q) < 1:
            q = timezone.now().date()
        queryset = Slip.objects.filter(today__schedule_date=q, game_fate=1).order_by('-score')

        if queryset.count() < 1:
            if q == timezone.now().date():
                q = timezone.now() - timezone.timedelta(days=1)
                queryset = Slip.objects.filter(today__schedule_date=q.date(), game_fate=1).order_by('-score')

        serializer = self.serializer_class(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RaffleWinnersView(APIView):
    serializer_class = RaffleWinnersSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        today = timezone.now()
        day_tosix = today.weekday() + 6  # add 6 to day of the week
        date_difference = day_tosix - 5  # minus by 5 to get sunday's day
        sunday_date = timezone.now() - timezone.timedelta(days=date_difference)  # get the most recent sundays date
        sunday_date = timezone.make_aware(
            timezone.datetime(sunday_date.year, sunday_date.month, sunday_date.day, 19, 58, 40, 0))
        if today.weekday() == 6 and timezone.now().time().hour > 18:
            queryset = RaffleWinners.objects.filter(created_at__date=timezone.now().date()).order_by('-id')
        else:
            queryset = RaffleWinners.objects.filter(created_at__date=sunday_date.date()).order_by('-id')

        serializer = self.serializer_class(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class EditMatches(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, pk):
        try:
            game = ActiveGame.objects.get(pk=pk)
        except ActiveGame.DoesNotExist:
            return Response(data={'response': 'Request not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        matches = request.data.get('matches')
        if len(matches) < 10:
            return Response(data={'non_field_errors': 'Request could not be validated please reload and try again.'},
                            status=status.HTTP_400_BAD_REQUEST)

        match_schedule_start_time = matches[0]['match_start_time']
        game.schedule_start_time = match_schedule_start_time
        game.save()

        for match in matches:
            match.update(match_start_time=dateparse.parse_datetime(match.get('match_start_time')),
                         over_two_five=round(float(match.get('over_two_five')), 2),
                         under_two_five=round(float(match.get('under_two_five')), 2),
                         home_team_odd=round(float(match.get('home_team_odd')), 2),
                         away_team_odd=round(float(match.get('away_team_odd')), 2),
                         even_odd=round(float(match.get('even_odd')), 2))

            event = Event.objects.get(pk=match['event'])
            home_team = Team.objects.get(name=match['home_team'])
            away_team = Team.objects.get(name=match['away_team'])

            try:
                match_details = Match.objects.get(pk=match['id'])
                match_details.event = event
                match_details.game_date = game
                match_details.over_two_five = match['over_two_five']
                match_details.under_two_five = match['under_two_five']
                match_details.home_team = home_team.name
                match_details.away_team = away_team.name
                match_details.home_team_odd = match['home_team_odd']
                match_details.away_team_odd = match['away_team_odd']
                match_details.even_odd = match['even_odd']
                match_details.match_start_time = match['match_start_time']
                match_details.save(update_fields=(
                'event', 'game_date', 'over_two_five', 'under_two_five', 'home_team', 'away_team', 'home_team_odd', 'away_team_odd', 'even_odd', 'match_start_time',))

            except Match.DoesNotExist:
                return Response(
                    data={'non_field_errors': 'Request could not be validated please reload and try again.'},
                    status=status.HTTP_400_BAD_REQUEST)

        return Response(data=True, status=status.HTTP_200_OK)


class RafflePlayers(APIView):
    serializer_class = RafflePlayerSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        try:
            raffle = WeekEndRaffle.objects.get(ended_at=timezone.now().date())
        except WeekEndRaffle.DoesNotExist:
            return Response(data=[], status=status.HTTP_200_OK)

        players = RafflePlayer.objects.filter(raffle=raffle.pk)

        serializer = self.serializer_class(players, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
