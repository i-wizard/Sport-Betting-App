from django.urls import path
from .views import UserCompleteProfileApiView, RequestOTPView, ResendOTP, UsersView, VerifyOTP, UserLoginView, \
    CreateUserView, UploadGravatar, UpdatePassword
from rest_framework_jwt.views import ObtainJSONWebToken

from .authSerializers import CustomJWTSerializer

app_name = 'auth'

urlpatterns = [
    path('', UsersView.as_view(), name='users_list'),
    path('request-otp', RequestOTPView.as_view(), name='request_otp'),
    path('resend-otp', ResendOTP.as_view(), name='resend_otp'),
    path('verify-otp', VerifyOTP.as_view(), name='verify_otp'),
    path('profile-completion', UserCompleteProfileApiView.as_view(), name='profile_completion'),
    path('login', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer), name='login'),
    path('session-login', UserLoginView.as_view(), name='login_session'),
    path('create', CreateUserView.as_view(), name='create_user'),
    path('upload-image-url', UploadGravatar.as_view()),
]
