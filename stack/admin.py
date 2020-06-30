from django.contrib import admin
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse, re_path
from django.utils.html import format_html

from account.models import Wallet
from users.models import User
from .models import ActiveGame, Game, Slip, Event, Match, WeekEndRaffle, RafflePlayer, RaffleWinners


class SlipAdmin(admin.ModelAdmin):
    list_display = (
        'today', 'slip_token', 'user', 'score', 'stake', 'game_fate', 'amount_won', 'is_smart_user', 'is_special',
        'played_at')
    list_filter = ('today', 'score', 'is_smart_user',)
    search_fields = ('slip_token', 'score',)
    filter_horizontal = ()
    ordering = ('score',)


class RaffleWinnersAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'created_at')


class GameAdmin(admin.ModelAdmin):
    list_display = (
        'slip', 'match', 'home_team_win', 'away_team_win', 'both_even', 'under_two_five', 'over_two_five', 'win',
        'is_smart')
    list_filter = ('win',)
    search_fields = ('slip',)
    filter_horizontal = ()
    ordering = ('-id',)


class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'event', 'game_date', 'home_team', 'away_team', 'home_team_score', 'away_team_score', 'role')
    list_filter = ('game_date',)
    search_fields = ('game_date',)
    filter_horizontal = ()
    ordering = ('-game_date',)


class ActiveGameAdmin(admin.ModelAdmin):
    # list_display = (
    #     'schedule_date', 'is_active', 'game_over', 'winners', 'space', 'decision', 'reset_actions')
    list_display = (
        'schedule_date', 'is_active', 'game_over', 'winners', 'space', 'decision')

    # def process_score_reset(self, request, game_id, *args, **kwargs):
    #     if request.method == 'GET':
    #         active_game = ActiveGame.objects.get(pk=game_id)
    #         slips = Slip.objects.filter(today=active_game.pk)
    #         Match.objects.filter(game_date=active_game.pk).update(home_team_score=0, away_team_score=0,
    #                                                               resulted=False)
    #
    #         for slip in slips:
    #             amount_won = slip.amount_won
    #             game_fate = slip.game_fate
    #
    #             slip_record = Slip.objects.get(pk=slip.pk)
    #             slip_record.score = 0
    #             slip_record.amount_won = 0
    #             slip_record.game_fate = 0
    #             slip_record.save(update_fields=('score', 'amount_won', 'game_fate',))
    #             Game.objects.filter(slip=slip.pk).update(points=0, win=False, settled=False, checked=False)
    #
    #             if active_game.decision:
    #                 if game_fate == 1:
    #                     amount = float(amount_won)
    #                     if not slip_record.is_special and not slip_record.is_smart_user:
    #                         slip_user_wallet = Wallet.objects.get(user=slip_record.user)
    #                         slip_user_wallet.balance = F('balance') - amount
    #                         slip_user_wallet.save(update_fields=('balance',))
    #
    #         active_game.game_over = False
    #         active_game.winners = 0
    #         active_game.amount_available = 100000
    #         active_game.space = 10
    #         active_game.decision = False
    #         active_game.save(update_fields=('game_over', 'winners', 'amount_available', 'space', 'decision',))
    #
    #         self.message_user(request, f'Success! all slips under {active_game.pk} has been successfully.')
    #         url = reverse(
    #             'admin:stack_activegame_change',
    #             args=[active_game.pk],
    #             current_app=self.admin_site.name,
    #         )
    #         return HttpResponseRedirect(url)
    #
    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         re_path(
    #             r'^(?P<game_id>.+)/reset-score/$',
    #             self.admin_site.admin_view(self.process_score_reset),
    #             name='reset-score',
    #         )
    #     ]
    #     return custom_urls + urls
    #
    # def reset_actions(self, obj):
    #     action = format_html(
    #         '<a class="button" href="{}">Reset Scores</a>',
    #         reverse('admin:reset-score', args=[obj.pk]),
    #     )
    #     return action
    #
    # reset_actions.short_description = 'Actions'
    # reset_actions.allow_tags = True


class WeekEndJackpotAdmin(admin.ModelAdmin):
    list_display = (
        'start_at', 'is_active', 'live', 'ended', 'start_at')


admin.site.register(ActiveGame, ActiveGameAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Slip, SlipAdmin)
admin.site.register(Event)
admin.site.register(Match, MatchAdmin)
admin.site.register(WeekEndRaffle, WeekEndJackpotAdmin)
admin.site.register(RafflePlayer)
admin.site.register(RaffleWinners, RaffleWinnersAdmin)
