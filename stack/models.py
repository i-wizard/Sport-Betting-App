from django.db import models
from django.db.models import Sum
from django.utils import timezone
from users.models import User


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    event_name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.event_name


class ActiveGame(models.Model):
    is_active = models.BooleanField(default=False)  # becomes true once first match has started
    game_over = models.BooleanField(default=False)  # becomes true once last match ends
    schedule_date = models.DateField(null=True, blank=True, db_index=True)  # the date the game will start
    schedule_start_time = models.DateTimeField(null=True, blank=True)  # the exact time the first game will start
    winners = models.IntegerField(default=0)  # number of winners of a particular game
    amount = models.DecimalField(max_digits=17, decimal_places=2, default=40000.00)
    amount_available = models.DecimalField(max_digits=17, decimal_places=2, default=40000.00)
    space = models.IntegerField(default=20)
    decision = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.schedule_date)

    @property
    def stake_sum(self):
        money = Slip.objects.filter(today=self.pk).aggregate(Sum('stake'))

        amount = 0

        if money['stake__sum'] is not None:
            amount = money['stake__sum']
        return amount

    @property
    def entries_count(self):
        entries = Slip.objects.filter(today=self.id).count()

        return entries


class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event')
    game_date = models.ForeignKey(ActiveGame, on_delete=models.CASCADE, related_name='game_date')
    home_team = models.CharField(max_length=150)
    away_team = models.CharField(max_length=150)
    home_team_score = models.IntegerField(default=0)
    away_team_score = models.IntegerField(default=0)
    home_team_odd = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    away_team_odd = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    under_two_five = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    over_two_five = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    even_odd = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    match_start_time = models.DateTimeField(null=True, blank=True)
    resulted = models.BooleanField(default=False)
    clubs_history = models.CharField(max_length=2000, null=True, blank=True)
    role = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{} vs {} - {}'.format(self.home_team, self.away_team, self.game_date.schedule_date)

    @property
    def both_team_score(self):
        return self.home_team_score + self.away_team_score


class Slip(models.Model):
    today = models.ForeignKey(ActiveGame, on_delete=models.CASCADE, null=True, blank=True, related_name='today')
    slip_token = models.CharField(max_length=50, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slip_user')
    score = models.IntegerField(default=0)
    stake = models.DecimalField(max_digits=17, decimal_places=2, default=0.00)
    amount_won = models.DecimalField(max_digits=17, decimal_places=2, default=0.00)
    game_fate = models.IntegerField(default=0, db_index=True)  # 0 for not decided, 1 for win, 2 for lose
    played_at = models.DateTimeField(default=timezone.now, db_index=True)
    is_special = models.BooleanField(default=False)
    is_smart_user = models.BooleanField(default=False)
    jackpot_check = models.BooleanField(default=False)

    def __str__(self):
        return self.slip_token

    @property
    def games(self):
        games = Game.objects.filter(slip=self.id).order_by('id')

        return games

    @property
    def active_game(self):
        return self.today


class Game(models.Model):
    slip = models.ForeignKey(Slip, models.CASCADE, related_name='slip')
    match = models.ForeignKey(Match, models.CASCADE, related_name='match')
    home_team_win = models.BooleanField(default=False)
    away_team_win = models.BooleanField(default=False)
    both_even = models.BooleanField(default=False)
    under_two_five = models.BooleanField(default=False)
    over_two_five = models.BooleanField(default=False)
    win = models.BooleanField(default=False)
    settled = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    is_smart = models.BooleanField(default=False)
    points = models.IntegerField(default=0)

    @property
    def match_details(self):
        return self.match


class WeekEndRaffle(models.Model):
    is_active = models.BooleanField(default=False, db_index=True)
    live = models.BooleanField(default=False, db_index=True)
    ended = models.BooleanField(default=False)
    start_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateField(null=True, blank=True)


class RafflePlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='raffle_player')
    raffle_hash = models.CharField(max_length=20, null=True, db_index=True)
    raffle = models.ForeignKey(WeekEndRaffle, on_delete=models.CASCADE)
    should_win = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.raffle.ended_at} - {self.raffle.pk} By {self.user.username}'


class RaffleWinners(models.Model):
    user = models.ForeignKey(RafflePlayer, on_delete=models.CASCADE, related_name='raffle_winner')
    created_at = models.DateTimeField(auto_now_add=True)
