from .base import *

ALLOWED_HOSTS = ['www.topplaysport.com', 'topplaysport.com', '54.208.188.177', '172.31.85.157', '3.225.117.198',
                 'toplaybalance-310072501.us-east-1.elb.amazonaws.com', '54.174.195.74']

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
#
SECURE_SSL_REDIRECT = True
#
SESSION_COOKIE_SECURE = True
#
CSRF_COOKIE_SECURE = True
#
SECURE_HSTS_SECONDS = 60
#
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#
SECURE_HSTS_PRELOAD = True
#
SECURE_CONTENT_TYPE_NOSNIFF = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # 'file': {
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'formatter': 'verbose',
        #     'filename': '/var/log/sport_betting.log',
        #     'maxBytes': 1024000,
        #     'backupCount': 3,
        #
        # },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ['console', 'mail_admins'],
            "propagate": True,
        },
    },
}

ADMINS = [('Confi', 'sudouser1443@gmail.com')]

DEFAULT_FROM_EMAIL = "sudouser1443@gmail.com"

# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = DEFAULT_FROM_EMAIL
