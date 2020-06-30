from stack.models import RafflePlayer
from utilities.helper import Helper


class RaffleIdGenerator:
    token = ''

    def __init__(self):
        self.token = self._token_check()

    def _token_check(self):
        token = self._token_gen()

        try:
            RafflePlayer.objects.get(raffle_hash=token)
        except RafflePlayer.DoesNotExist:
            return token

        return self._token_check()

    def _token_gen(self):
        helpers = Helper()
        return helpers.token_gen(length=6, ext='int')
