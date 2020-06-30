from django.urls import path

from referral.views import referral_details
from utilities.general_middleware import AuthCheckMiddleware
from django.utils.decorators import decorator_from_middleware

app_name = 'referral'

user_auth_decorator = decorator_from_middleware(AuthCheckMiddleware)

urlpatterns = [
    path('', user_auth_decorator(referral_details), name='index'),
]
