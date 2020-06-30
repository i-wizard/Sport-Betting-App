import environ
import os


class SiteENVDetails:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    _env = environ.Env()
    _env.read_env(os.path.join(BASE_DIR, '.env'))

    def get_site_name(self):
        return self._env('SITE_NAME')

    def get_site_url(self):
        return self._env('SITE_URL')

    def get_sms_key(self):
        return self._env('SMS_API_KEY')


get_site_details = SiteENVDetails()
