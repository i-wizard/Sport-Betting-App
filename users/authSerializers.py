"""All auth related things are serialized here. Once OTP has been verified the user will be taken to 
UserProfileSerializer will take care of the details completion so the user can gain access the his/her account. """

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from random import randint
from django.utils import timezone

from account.models import Wallet
from core.models import GameSetting
from referral.models import Referral
from utilities.helper import Mailer, Helper
from utilities.referral_gen import ReferralTokenGenerator
from utilities.site_details import get_site_details
from .models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

helpers = Mailer()
helper_func = Helper()


class UserProfileCreationSerializer(serializers.ModelSerializer):
    retype_password = serializers.CharField(required=False, allow_blank=False)
    referral_code = serializers.CharField(required=False, allow_blank=True)

    class Meta(object):
        model = User
        exclude = ('calling_code',)

    def validate(self, cleaned_data):
        password = cleaned_data.get('password').lower()
        retype_password = cleaned_data.get('retype_password').lower()
        referral_code = cleaned_data.get('referral_code').lower()

        if len(password) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters.")

        if not retype_password == password:
            raise serializers.ValidationError("Password and retype password does not match.")

        if referral_code and len(referral_code) > 0:
            try:
                User.objects.get(referral_code=referral_code)
            except User.DoesNotExist:
                raise serializers.ValidationError("Your referrer is not valid.")

        return cleaned_data

    def update(self, instance, validated_data):
        int_rand = randint(1, 19)
        img_url = 'http://{}/static/images/logos/teams/team-{}.png'.format(get_site_details.get_site_url(), randint(1, 19))
        # print("IMAGE THINGS: {}".format(img_url))
        image = helper_func.urls_image_upload(img_url)

        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.set_password(validated_data.get('password').lower())
        instance.is_active = True

        referral_gen = ReferralTokenGenerator()

        instance.referral_code = referral_gen.token.lower()

        if validated_data.get('referral_code'):
            instance.referred = True

        instance.save()

        instance.profile_image.save(image[0], image[1], save=True)

        if instance.referred:
            referrer = User.objects.get(referral_code=validated_data.get('referral_code').lower())

            Referral.objects.create(referrer=referrer, user=instance)
            helpers.send_referrer_msg(referrer, instance.username)

        # create wallet for the user after account details has been completed

        wallet = Wallet.objects.create(user=instance)

        game_setting = GameSetting.objects.filter()[0]

        if game_setting:
            if timezone.now().date() <= game_setting.trial_ending:
                wallet.bonus_balance = 1000
                wallet.save(update_fields=('bonus_balance',))

        # send email to the user for successful registration
        helpers.send_first_time_mail(instance.email, instance.username)

        return instance


class RequestOtpSerializer(serializers.Serializer):
    # calling_code = serializers.IntegerField()
    phone = serializers.CharField(max_length=50)


class VerifyOTPSerializer(serializers.Serializer):
    # calling_code = serializers.IntegerField()
    phone = serializers.CharField(max_length=50)
    token = serializers.IntegerField(required=False)

    def validate(self, cleaned_data):
        token = cleaned_data.get('token')

        if not token:
            raise serializers.ValidationError("Please enter the token sent to your phone number.")

        return cleaned_data

    def create(self, validated_data):
        phone = validated_data['phone']
        if not phone[0] == 0:
            phone = '{}{}'.format(0, phone)
        user = User.objects.create(phone=phone)
        return user


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True)

    def validate(self, cleaned_data):
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password').lower()

        if len(password) < 1 or len(phone) < 1:
            raise serializers.ValidationError("Please enter both phone number and password.")

        if not User.objects.filter(phone=phone):
            raise serializers.ValidationError("Sorry! No such user exist.")

        user_details = User.objects.filter(phone=phone, is_active=False)
        if user_details.exists():
            if user_details[0].username:
                raise serializers.ValidationError("Sorry! This account has been blocked.")

        if User.objects.filter(phone=phone, is_deleted=True).exists():
            raise serializers.ValidationError("This account has been deleted from our system.")

        return cleaned_data


class CustomJWTSerializer(JSONWebTokenSerializer):
    phone = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True)

    username_field = 'phone'

    def validate(self, attrs):

        password = attrs.get("password").lower()
        phone = attrs.get("password")

        if len(password) < 1 or len(phone) < 1:
            msg = {
                "non_field_errors": "Please enter both phone number and password."
            }

        if not User.objects.filter(phone=phone):
            msg = {
                "non_field_errors": "Sorry! No such user exist."}

        if User.objects.filter(phone=phone, is_active=False):
            msg = {
                "non_field_errors": "Sorry! This account has been blocked."}

        if User.objects.filter(phone=phone, is_deleted=True):
            msg = {
                "non_field_errors": "This account has been deleted from our system."}

        user_obj = User.objects.filter(phone=attrs.get("phone")).first()
        if user_obj is not None:
            credentials = {
                'phone': user_obj.phone,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    payload = jwt_payload_handler(user)
                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = {
                        "non_field_errors": "phone and password do not match."
                    }
                    raise serializers.ValidationError(msg)

            else:
                msg = {
                    "non_field_errors": "Both phone number and password is required."
                }
                raise serializers.ValidationError(msg)

        else:
            msg = {
                "non_field_errors": "Account does not exists."}
            raise serializers.ValidationError(msg)
