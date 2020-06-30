from .base import *

# CORS_ORIGIN_WHITELIST = [
#     "http://127.0.0.1:3000",
#     "http://localhost:3000",
#     "http://localhost:8080"
# ]

STATIC_ROOT = None

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'public')
]
