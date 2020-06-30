from stack.models import Slip
from utilities.helper import Helper


class SlipTokenGenerator:
    token = ''

    def __init__(self):
        self.token = self._token_check()

    def _token_check(self):
        token = self._token_gen()

        try:
            Slip.objects.get(slip_token=token)
        except Slip.DoesNotExist:
            return token

        return self._token_check()

    def _token_gen(self):
        helpers = Helper()
        return helpers.token_gen(length=8, ext='alphanum')
