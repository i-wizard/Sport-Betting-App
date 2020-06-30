from django.db import models

from stack.models import Team
from users.models import User

QUESTION_STATUS = (
    ('open', 'OPEN'),
    ('canceled', 'CANCELED'),
    ('resulted', 'RESULTED'),
)

ATTEMPT_STATUS = (
    ('won', 'WON'),
    ('lose', 'LOSE'),
)


class Question(models.Model):
    event = models.CharField(max_length=100)
    team_a_logo = models.CharField(max_length=1000)
    team_b_logo = models.CharField(max_length=1000)
    team_a = models.CharField(max_length=100)
    team_b = models.CharField(max_length=100)
    team_a_score = models.CharField('team a score', null=True, blank=True, max_length=10)
    team_b_score = models.CharField('team b score', null=True, blank=True, max_length=10)
    total_corner_kicks = models.CharField('total corner kicks', null=True, blank=True, max_length=10)
    total_cards = models.CharField('total cards', null=True, blank=True, max_length=10)
    status = models.CharField(max_length=10, choices=QUESTION_STATUS,
                              default='open')
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('closed_at',)

    @property
    def num_players(self):
        return Attempt.objects.filter(question=self.pk).count()

    @property
    def num_winners(self):
        return Attempt.objects.filter(question=self.pk, status='won').count()

    @property
    def num_loses(self):
        return Attempt.objects.filter(question=self.pk, status='lose').count()


class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    team_a_score = models.CharField(null=True, blank=True, max_length=10)
    team_b_score = models.CharField(null=True, blank=True, max_length=10)
    total_corner_kicks = models.CharField(null=True, blank=True, max_length=10)
    total_cards = models.CharField(null=True, blank=True, max_length=10)
    status = models.CharField(max_length=10, choices=ATTEMPT_STATUS, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    @property
    def teams_score(self):
        if self.question.status == 'resulted':
            if self.team_a_score == self.question.team_a_score and self.team_b_score == self.question.team_b_score:
                return 'won'
            else:
                return 'lose'
        return ''

    @property
    def teams_corner_kicks(self):
        if self.question.status == 'resulted':
            if self.total_corner_kicks == self.question.total_corner_kicks:
                return 'won'
            else:
                return 'lose'
        return ''

    @property
    def total_cards_result(self):
        if self.question.status == 'resulted':
            if self.total_cards == self.question.total_cards:
                return 'won'
            else:
                return 'lose'
        return ''
