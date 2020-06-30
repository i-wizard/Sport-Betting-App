from django.db.models import F

from account.models import Wallet
from trivia.models import Attempt


class Marking:
    def credit_user(self, user=None):
        user_wallet = Wallet.objects.get(user=user.pk)
        user_wallet.balance = F('balance') + 10000
        user_wallet.save(update_fields=('balance',))

    def __init__(self, question=None):
        attempts = Attempt.objects.filter(question=question.pk)

        for attempt in attempts:
            if attempt.total_cards == question.total_cards and attempt.team_a_score == question.team_a_score \
                    and attempt.team_b_score == question.team_b_score and attempt.total_corner_kicks == question.total_corner_kicks:
                attempt.status = 'won'
                self.credit_user(attempt.user)
            else:
                attempt.status = 'lose'

            attempt.save(update_fields=('status',))
