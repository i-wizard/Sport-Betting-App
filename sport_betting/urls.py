from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
# from django.conf.urls.static import static
from core.views import homepage, ref_homepage, privacy, terms_condition_view
from users.views import (login_view, register_view, logout_handler, ProfileDetails, UpdatePassword,
                         PasswordResetView, LostPassword)
from stack.views import mybets_view, slip_details_view, slip_details_q_view, winners_list, jackpot_winners_list
from support.views import support_view, Issue
from utilities.general_middleware import AuthCheckMiddleware, ButAdminMiddleware
from django.utils.decorators import decorator_from_middleware

from .view import faqs_view, how_to_play

user_auth_decorator = decorator_from_middleware(AuthCheckMiddleware)
but_admin_decorator = decorator_from_middleware(ButAdminMiddleware)

urlpatterns = [
    path('twisted/app/admin/', admin.site.urls),
    path('', but_admin_decorator(homepage), name="HomePage"),
    path('ref/<str:token>', but_admin_decorator(ref_homepage)),
    path('login', login_view, name="LoginPage"),
    path('logout', logout_handler, name="logoutPage"),
    path('register', register_view, name="RegistrationPage"),
    path('users/', include('users.urls')),
    # path('send-sms', phone_verification, name='send'),
    path('core/', include('core.urls')),
    path('trivia/', include('trivia.urls')),
    path('betting/', include('stack.urls')),
    path('account/', include('account.urls')),
    path('support/', include('support.urls')),
    path('admin/', include('admin.urls')),

    # logged in users routes
    path('bets', user_auth_decorator(mybets_view), name='mybets'),
    path('profile', user_auth_decorator(ProfileDetails.as_view()), name='profilePage'),
    path('update-password', user_auth_decorator(UpdatePassword.as_view()), name='updatePassword'),

    path('referrals', include('referral.urls')),

    path('slip/<slug:token>', slip_details_view, name='slip_details'),
    path('slip', slip_details_q_view, name='slip_details_q'),
    path('bets/winners', winners_list, name='winners_chart'),
    path('jackpot/winners', jackpot_winners_list, name='jackpot_winners'),
    path('faqs', faqs_view, name='Faqs'),
    path('how-to-play', how_to_play, name='HowToPlay'),
    path('support', Issue.as_view(), name='Support'),
    path('privacy', privacy, name='Privacy'),
    path('terms-and-condition', terms_condition_view, name='Terms'),
    path('lost-password', LostPassword.as_view(), name='lostPassword'),
    re_path(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            PasswordResetView.as_view(), name='password_reset'),
    path('password-reset', PasswordResetView.as_view(), name='password_reset_form'),

]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^assets/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
