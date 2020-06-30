from users.models import User
from utilities.helper import Helper


class ReferralTokenGenerator:
    token = ''

    def __init__(self):
        self.token = self._token_check()

    def _token_check(self):
        token = self._token_gen().lower()

        try:
            User.objects.get(referral_code=token)
        except User.DoesNotExist:
            return token

        return self._token_check()

    def _token_gen(self):
        helpers = Helper()
        return helpers.token_gen(length=8, ext='alphanum')
