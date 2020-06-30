from authy.api import AuthyApiClient
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect
from rest_framework import status, permissions, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login, logout
from django.views import View

from users.forms import ForgotResetForm, ForgotPasswordForm
from users.models import User
from .authSerializers import RequestOtpSerializer, UserProfileCreationSerializer, VerifyOTPSerializer, \
    UserLoginSerializer
from .userSerializers import UserListSerializers, AdminCreateUserSerializer
from utilities.helper import Helper, LargeResultsSetPagination
from utilities.account import password_reset_link, password_reset_token

helpers = Helper()
api = AuthyApiClient(helpers.SMS_API_KEY)
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class UserCompleteProfileApiView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        user_data = request.data

        try:
            user = User.objects.get(phone=request.data['phone'])
        except User.DoesNotExist:
            return Response(data={'non_field_errors': 'Request could not be completed at this time.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.email and user.username:
            return Response(data={'non_field_errors': 'Details already set please proceed..'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileCreationSerializer(user, data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        login(request, user)
        payload = jwt_payload_handler(user)
        return Response(data={
            'is_staff': user.is_staff,
            'token': jwt_encode_handler(payload)
        }, status=status.HTTP_200_OK)


class RequestOTPView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RequestOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if User.objects.filter(phone=serializer.validated_data['phone']):
            return Response(data={'non_field_errors': 'A user with this phone number already exist.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # User.objects.create(phone=serializer.data['phone'], calling_code=serializer.data['calling_code'])

        # api.phones.verification_start(serializer.validated_data['phone'], serializer.validated_data['calling_code'],
        #                               via='sms')

        user = User.objects.create(phone=serializer.data['phone'])

        user_data = {
            'phone': user.phone,
            # 'calling_code': user.calling_code,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_deleted': user.is_deleted,
            'date_joined': user.date_joined
        }

        return Response(
            data=user_data,
            status=status.HTTP_200_OK
        )


class ResendOTP(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RequestOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if User.objects.filter(phone=serializer.validated_data['phone'], is_active=True):
            return Response(data={'non_field_errors': 'Sorry! This account has already been verified.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # api.phones.verification_start(serializer.validated_data['phone'], serializer.validated_data['calling_code'],
        #                               via='sms')

        return Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK
        )


class VerifyOTP(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # verification = api.phones.verification_check(
        #     serializer.validated_data['phone'],
        #     serializer.validated_data['calling_code'],
        #     serializer.validated_data['token']
        # )

        # if verification.ok():
        #     user = serializer.save()
        #
        #     user_data = {
        #         'phone': user.phone,
        #         # 'calling_code': user.calling_code,
        #         'is_active': user.is_active,
        #         'is_staff': user.is_staff,
        #         'is_deleted': user.is_deleted,
        #         'date_joined': user.date_joined
        #     }
        #
        #     return Response(
        #         data=user_data,
        #         status=status.HTTP_200_OK
        #     )
        # else:
        #     return Response(data={'non_field_errors': 'Sorry! This token is either not valid or has expired.'},
        #                     status=status.HTTP_400_BAD_REQUEST)


class UsersView(generics.ListAPIView):
    queryset = User.objects.all().filter(is_staff=False).order_by('-id')
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UserListSerializers
    pagination_class = LargeResultsSetPagination


class UserLoginView(APIView):
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        credentials = {
            'phone': serializer.validated_data['phone'],
            'password': serializer.validated_data['password'].lower()
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                login(request, user)
                return Response(data={
                    'is_staff': user.is_staff,
                }, status=status.HTTP_200_OK)
            else:
                user = User.objects.get(phone=serializer.validated_data['phone'])

                if not user.is_active:
                    user_data = {
                        'phone': user.phone,
                        # 'calling_code': user.calling_code,
                        'is_active': user.is_active,
                        'is_staff': user.is_staff,
                        'is_deleted': user.is_deleted,
                        'date_joined': user.date_joined
                    }
                    return Response(data=user_data, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                return Response(data={'non_field_errors': 'Phone number and password does not match any record.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.get(phone=serializer.validated_data['phone'])

            if not user.is_active:
                user_data = {
                    'phone': user.phone,
                    # 'calling_code': user.calling_code,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_deleted': user.is_deleted,
                    'date_joined': user.date_joined
                }
                return Response(data=user_data, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            return Response(data={'non_field_errors': 'Please enter your phone number and password.'},
                            status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = AdminCreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return JsonResponse(serializer.data, status=201)


class LostPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        pass


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'auth/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'auth/register.html')


def logout_handler(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')


class ProfileDetails(View):
    def get(self, request):
        profile_details = User.objects.get(pk=request.user.pk)

        context = {
            'profile_details': profile_details
        }

        return render(request, 'profile/details.html', context)

    def post(self, request):
        user = User.objects.get(pk=request.user.pk)
        # user.phone = phone

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")
            user.save()
            messages.success(request, 'Profile updated successfully.')

        profile_details = User.objects.get(pk=request.user.pk)

        context = {
            'profile_details': profile_details,
            'form': []
        }

        return render(request, 'profile/details.html', context)


class UploadGravatar(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = User.objects.get(id=request.user.id)

        image = helpers.urls_image_upload(request.data.get('img_url'))

        if len(image):
            user.profile_image.save(image[0], image[1], save=True)

        return Response(
            data={'response': "GOOD"},
            status=status.HTTP_200_OK
        )


class UpdatePassword(View):
    form = ForgotResetForm

    def post(self, request):
        self.form = self.form(data=request.POST)
        profile_details = User.objects.get(pk=request.user.pk)

        if self.form.is_valid():
            if profile_details.check_password(request.POST.get('current_password', '').lower()):
                profile_details.set_password(self.form.cleaned_data.get('password').lower())
                profile_details.save()

                messages.success(request, 'Password updated successfully.')
            else:
                messages.warning(request, 'Old password is not correct.')

        context = {
            'profile_details': profile_details,
            'form': self.form
        }

        # print(self.form)

        return render(request, 'profile/details.html', context)


class LostPassword(View):
    form = ForgotPasswordForm

    def get(self, request):
        return render(request, 'auth/password/lost.html', {'form': self.form})

    def post(self, request):
        self.form = self.form(data=request.POST)

        if self.form.is_valid():
            try:
                user = User.objects.get(email=self.form.cleaned_data.get('email'))
            except User.DoesNotExist:
                messages.warning(request, 'A user with this email address does not exist.')

                return render(request, 'auth/password/lost.html', {'form': self.form})

            password_reset_link(request, user)
            messages.success(request, 'Password reset link has been sent to your email address.')
        # print(self.form.errors)
        return render(request, 'auth/password/lost.html', {'form': self.form})


class PasswordResetView(View):
    form = ForgotResetForm
    form_success = False

    def get(self, request, uidb64=None, token=None):
        if uidb64 is None or token is None:
            raise Http404

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            return render(request, 'auth/password/reset.html',
                          {'success': self.form_success, 'user': user.pk, 'form': self.form})
        else:
            raise Http404

    def post(self, request):
        self.form = self.form(data=request.POST)

        if self.form.is_valid():
            try:
                user = User.objects.get(pk=request.POST['user'])
            except User.DoesNotExist:
                messages.warning(request, 'Request could not be validated.')

                return render(request, 'auth/password/reset.html',
                              {'success': self.form_success, 'user': request.POST['user'], 'form': self.form})

            user.set_password(self.form.cleaned_data.get("password").lower())
            user.save()

            self.form_success = True
            messages.success(request, 'Password changed successfully.')

        return render(request, 'auth/password/reset.html',
                      {'success': self.form_success, 'user': request.POST['user'], 'form': self.form})
