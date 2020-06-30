from random import randint
from django.db.models import F

from core.models import GameSetting
from utilities.raffle_id import RaffleIdGenerator
from utilities.random_choices import ChoiceRandomization
from utilities.slip_token import SlipTokenGenerator
from account.models import Wallet, Withdrawal
from stack.models import ActiveGame, Match, Slip, Game, RafflePlayer, WeekEndRaffle, RaffleWinners
from users.models import User
from utilities.helper import WinnersSort, Mailer
from django.utils import timezone, dateparse
from paystackpy import Transaction, Transfer


class UpdateApi:
    today = timezone.now().date()

    def today_game(self):
        try:
            today_game = ActiveGame.objects.get(schedule_date=self.today)
        except ActiveGame.DoesNotExist:
            today_game = None

        return today_game

    def end_today_game(self):
        if self.today_game():
            last_game = Match.objects.get(
                role=10, game_date=self.today_game().pk)

            if last_game.resulted:
                active_game = ActiveGame.objects.get(pk=self.today_game().pk)
                active_game.game_over = True
                active_game.save(update_fields=('game_over',))

    def start_today_game(self):
        if self.today_game() is not None and not self.today_game().is_active:
            if timezone.now().replace(microsecond=0, second=0) >= self.today_game().schedule_start_time:
                game_self = ActiveGame.objects.get(id=self.today_game().id)
                game_self.is_active = True
                game_self.save(update_fields=('is_active',))

                # Add admin users to game
                total_bets = Slip.objects.filter(
                    today=self.today_game().pk).count()
                try:
                    game_setting = GameSetting.objects.get()
                except GameSetting.DoesNotExist:
                    return False

                if game_setting.min_user_limit > total_bets:
                    special_users = User.objects.filter(
                        is_moderator=True, is_active=True)
                    if special_users.count():
                        matches = Match.objects.filter(
                            game_date=self.today_game().pk)

                        for user in special_users:
                            slip_token = SlipTokenGenerator().token
                            time = timezone.now() - timezone.timedelta(hours=randint(1, 3))
                            new_slip = Slip.objects.create(today=self.today_game(), user=user, stake=200,
                                                           played_at=time,
                                                           slip_token=slip_token, is_special=True)

                            for match in matches:
                                rand_choice = randint(0, 1)
                                choices = [True, False]
                                picked_choice = choices[rand_choice]
                                point_picked_choice = ChoiceRandomization()
                                Game.objects.create(slip=new_slip, match=match,
                                                    home_team_win=point_picked_choice.choice_one,
                                                    away_team_win=point_picked_choice.choice_two,
                                                    both_even=point_picked_choice.choice_three,
                                                    under_two_five=picked_choice,
                                                    over_two_five=not picked_choice)

                        special_slips = Slip.objects.filter(
                            today=self.today_game().pk, is_special=True)

                        if special_slips.count() > game_setting.num_smart_users:
                            smart_slips = []

                            for special_slip in special_slips:
                                if len(smart_slips) < game_setting.num_smart_users:
                                    selection_pattern = randint(
                                        0, (special_slips.count() - 1))

                                    if special_slips[selection_pattern] not in smart_slips:
                                        smart_slips.append(
                                            special_slips[selection_pattern])

                                else:
                                    break

                            for smart_slip in smart_slips:
                                slip = Slip.objects.get(pk=smart_slip.pk)
                                slip.is_smart_user = True
                                slip.save(update_fields=('is_smart_user',))

                                Game.objects.filter(
                                    slip=slip.pk).update(is_smart=True)

    # fire an event

    def alter_slip(self):
        if self.today_game():
            total_amount = 40000
            amount_per_winner = 2000
            game_setting = GameSetting.objects.filter()[0]

            if game_setting:
                if timezone.now().date() <= game_setting.trial_ending:
                    total_amount = 20000
                    amount_per_winner = 1000

            if self.today_game().game_over and self.today_game().amount_available == total_amount and self.today_game().space == 20 and self.today_game().decision is False:
                slips = Slip.objects.filter(today=self.today_game().pk, game_fate=0) \
                    .values('id', 'user', 'slip_token', 'score', 'game_fate', 'amount_won').order_by('-score')

                sotter = WinnersSort()

                map = []

                if slips.count():
                    for slip in slips:
                        search_record = sotter.search(
                            slip['score'], map, 'score')

                        if search_record and search_record[0]:
                            map[search_record[1]].append(slip)
                        else:
                            map.append([slip])

                    space_available = int(self.today_game().space)
                    amount_available = self.today_game().amount_available
                    no_winners = self.today_game().winners

                    amount_used = 0

                    for group in map:
                        amount_to_receive_in_tense = sotter.amount_to_tens(
                            len(group)) * 200

                        if game_setting:
                            if timezone.now().date() <= game_setting.trial_ending:
                                amount_to_receive_in_tense = sotter.amount_to_tens(
                                    len(group)) * 200

                        mailer = Mailer()

                        if space_available >= len(
                                group) and space_available > 0 and amount_available >= amount_to_receive_in_tense:
                            # print("SPACE ONE: {}".format(group[0]['score']))
                            # print("GROUP: {}".format(len(group)))
                            # print("SPACE: {}".format(space_available))
                            # (amount_available * amount_to_receive_in_tense) // 100
                            amount_payable = amount_per_winner
                            space_available -= len(group)
                            amount_won = amount_payable  # / len(group)
                            amount_available -= (amount_payable * len(group))
                            no_winners = no_winners + len(group)
                            # print("GROUP MEMBERS SCORE: {}".format(group[0]['score']))

                            for slip in group:
                                amount_used += amount_won
                                user_slip = Slip.objects.get(pk=slip['id'])
                                user_slip.amount_won = amount_won
                                user_slip.game_fate = 1
                                user_slip.save(update_fields=(
                                    'amount_won', 'game_fate',))

                                if not user_slip.is_special:
                                    user_wallet = Wallet.objects.get(
                                        user=user_slip.user.pk)
                                    user_wallet.balance = F(
                                        'balance') + user_slip.amount_won
                                    user_wallet.save(
                                        update_fields=('balance',))

                                    # mailer.send_winning_msg(user_slip.user)

                        elif space_available > 0 and len(group) > space_available and amount_available > 1:
                            # print("SPACE TWO: {}".format(group[0]['score']))
                            # print("GROUP: {}".format(len(group)))
                            # print("SPACE: {}".format(space_available))

                            amount_payable = amount_available / len(group)
                            space_available = 0
                            # (amount_payable * len(group))
                            amount_available = 0
                            amount_won = amount_payable
                            no_winners += len(group)

                            for slip in group:
                                amount_used += amount_won
                                user_slip = Slip.objects.get(pk=slip['id'])
                                user_slip.amount_won = amount_won
                                user_slip.game_fate = 1
                                user_slip.save(update_fields=(
                                    'amount_won', 'game_fate',))

                                if not user_slip.is_special:
                                    user_wallet = Wallet.objects.get(
                                        user=user_slip.user.pk)
                                    user_wallet.balance = F(
                                        'balance') + user_slip.amount_won
                                    user_wallet.save(
                                        update_fields=('balance',))

                                    # mailer.send_winning_msg(user_slip.user)

                    mailer = Mailer()
                    # mailer.send_my_mail(amount_used)

                    active_game = ActiveGame.objects.get(
                        pk=self.today_game().pk)
                    active_game.space = space_available
                    active_game.amount_available = amount_available
                    active_game.winners = F('winners') + no_winners
                    active_game.decision = True
                    active_game.save(update_fields=(
                        'space', 'amount_available', 'winners', 'decision',))

            elif self.today_game().game_over and self.today_game().decision:
                Slip.objects.filter(today=self.today_game().pk,
                                    game_fate=0).update(game_fate=2)

    def add_raffle_members(self):
        today = timezone.now()
        day_tosix = today.weekday() + 6  # add 6 to day of the week
        date_difference = day_tosix - 5  # minus by 5 to get sunday's day
        # get the most recent sundays date
        sunday_date = timezone.now() - timezone.timedelta(days=date_difference)
        sunday_date = timezone.make_aware(
            timezone.datetime(sunday_date.year, sunday_date.month, sunday_date.day, 20, 5, 0, 0))

        if today.weekday() == 6:
            if timezone.make_aware(timezone.datetime(today.year, today.month, today.day, 19, 57, 0,
                                                     0)) <= today < timezone.make_aware(
                timezone.datetime(today.year, today.month, today.day, 20, 5, 0,
                                  0)):
                return False

        slips = Slip.objects.filter(played_at__gte=sunday_date, is_special=False,
                                    jackpot_check=False).values('id', 'user', 'slip_token', 'score', 'game_fate',
                                                                'amount_won')

        sotter = WinnersSort()
        map = []

        if slips.count():
            for slip in slips:
                #  check if there is any raffle for this week or start one if none
                try:
                    raffle = WeekEndRaffle.objects.get(is_active=True)
                except WeekEndRaffle.DoesNotExist:
                    raffle = WeekEndRaffle.objects.create(is_active=True)

                if not RafflePlayer.objects.filter(user=slip['user'], raffle=raffle.pk).count():
                    # check if the user has played upto 5 games that week
                    if slips.filter(user=slip['user']).count() >= 5:
                        search_record = sotter.search(
                            slip['user'], map, 'user')

                        if search_record and search_record[0]:
                            map[search_record[1]].append(slip)
                        else:
                            map.append([slip])

                        # print("MAP RECORD: {}".format(map))

                        selections = []

                        for group in map:
                            selections.append(group[0])

                        # print("SELECTIONS: {}".format(selections))

                        for selection in selections:
                            raffle_id = RaffleIdGenerator().token
                            user = User.objects.get(pk=selection['user'])
                            raffle_check = RafflePlayer.objects.filter(
                                user=user, raffle=raffle.pk)
                            # check_slip_won = Slip.objects.filter(played_at__gte=sunday_date, user=user.pk, game_fate=1)
                            if not raffle_check:
                                user_raffle = RafflePlayer.objects.create(user=user, raffle_hash=raffle_id,
                                                                          raffle=raffle)
                                if not user.is_moderator:
                                    wallet = Wallet.objects.get(user=user.pk)
                                    wallet.bonus_balance = F(
                                        'bonus_balance') + 200
                                    wallet.save()

                                mailer = Mailer()
                                mailer.send_raffle_player(user, raffle_id)

    def end_raffle_draw(self):
        week_day = timezone.now().weekday()

        # if week_day is 6:
        # print(week_day)
        if week_day == 6:
            if timezone.make_aware(
                        timezone.datetime(timezone.now().year, timezone.now().month, timezone.now().day, 19, 58, 0,
                                          0)) <= timezone.now() < timezone.make_aware(
                    timezone.datetime(timezone.now().year, timezone.now().month, timezone.now().day, 19, 59, 50, 0)):
                try:
                    raffle = WeekEndRaffle.objects.get(is_active=True)
                except WeekEndRaffle.DoesNotExist:
                    return False

                # players = RafflePlayer.objects.filter(raffle_id=raffle.pk, should_win=False)
                players = RafflePlayer.objects.filter(raffle=raffle.pk)

                Slip.objects.filter(jackpot_check=False).update(
                    jackpot_check=True)

                # if players.count():
                try:
                    game_setting = GameSetting.objects.get()
                except GameSetting.DoesNotExist:
                    return False

                winners_limit = 20
                topplay_limit = game_setting.num_jackpot_winners
                selections = []
                mod_users = User.objects.filter(is_moderator=True, is_active=True)[
                                                :(topplay_limit+1)]
                moderators = []

                for mod_user in mod_users:
                    raffle_id = RaffleIdGenerator().token
                    player = RafflePlayer.objects.create(
                        user=mod_user, raffle_hash=raffle_id, raffle=raffle)
                    moderators.append(player)

                if len(moderators) < topplay_limit:
                    topplay_limit = len(moderators)

                selected_mods = []

                for mod in moderators:
                    if len(selected_mods) < topplay_limit:
                        random_user_id = randint(0, (topplay_limit - 1))
                        if moderators[random_user_id] not in selected_mods:
                            selected_mods.append(
                                moderators[random_user_id])
                    else:
                        break

                if len(selected_mods) > 0:
                    for mod in selected_mods:
                        selections.append(mod)

                if len(selections) < winners_limit:
                    for player in players:
                        if len(selections) < winners_limit:
                            random_user_id = randint(
                                0, (winners_limit - 1))
                            if players[random_user_id] not in selections:
                                selections.append(players[random_user_id])
                        else:
                            break

                for selection in selections:
                    RaffleWinners.objects.create(user=selection)

                    if not selection.user.is_moderator:
                        user = User.objects.get(selection.user.pk)
                        mailer = Mailer()
                        # mailer.send_raffle_winner(user)
                        user_wallet = Wallet.objects.get(user=user.pk)
                        user_wallet.balance = F('balance') + 1000
                        user_wallet.save(update_fields=('balance',))

                raffle.is_active = False
                raffle.ended = True
                raffle.ended_at = timezone.now().date()
                raffle.live = False
                raffle.save(update_fields=(
                    'is_active', 'ended', 'ended_at', 'live',))

    def init_game_setting(self):
        try:
            GameSetting.objects.get()
        except GameSetting.DoesNotExist:
            GameSetting.objects.create(num_smart_users=8, min_user_limit=600)

    def check_payments(self):
        withdrawals = Withdrawal.objects.filter(
            is_confirmed=False, transaction_status=0)

        if withdrawals.count():
            for withdrawal in withdrawals:
                withdrawal_check = Transfer().get_transfer(
                    ref_or_code=withdrawal.transaction_uid)
                withdrawal = Withdrawal.objects.get(pk=withdrawal.pk)
                wallet = Wallet.objects.get(pk=withdrawal.wallet.pk)

                if withdrawal_check[1]:
                    if withdrawal_check[3]['status'] == 'success':
                        withdrawal.transaction_status = 1
                        withdrawal.is_confirmed = True
                else:
                    withdrawal.transaction_status = 2
                    wallet.balance = F('balance') + withdrawal.amount
                    wallet.save(update_fields=('balance',))

                withdrawal.save()
