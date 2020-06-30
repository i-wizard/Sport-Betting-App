from random import randint
from rest_framework import serializers
from account.models import Wallet
from utilities.helper import Helper
from utilities.site_details import get_site_details
from .models import User

helper_func = Helper()


class UserListSerializers(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = '__all__'


class AdminCreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, error_messages={"blank": "Please enter username",
                                                                    "unique": "User name already in use"})
    email = serializers.CharField(required=True, error_messages={
        "blank": "Please enter a valid email address",
        "unique": "A user with this email address already exist"})
    phone = serializers.CharField(required=True, error_messages={"blank": "Please enter phone number",
                                                                 "unique": "Phone number already taken"})
    password = serializers.CharField(required=True, error_messages={"blank": "Please enter user password"})

    class Meta(object):
        model = User
        fields = '__all__'

    def validate(self, attrs):
        username = attrs.get("username")
        phone = attrs.get("phone")
        email = attrs.get("email")

        if User.objects.filter(username=username):
            raise serializers.ValidationError("Username already in use.")

        if User.objects.filter(email=email):
            raise serializers.ValidationError("Email address already taken.")

        if User.objects.filter(phone=phone):
            raise serializers.ValidationError("Phone number already taken.")

        return attrs

    def create(self, validated_data):
        user = User.objects.create(phone=validated_data.get('phone'), calling_code=validated_data.get('calling_code'),
                                   username=validated_data.get('username'), email=validated_data.get('email'),
                                   is_active=True, is_moderator=True)

        user.set_password(validated_data.get('password').lower())
        user.save()

        img_url = 'http://{}/static/images/logos/teams/team-{}.png'.format(get_site_details.get_site_url(), randint(1, 19))
        image = helper_func.urls_image_upload(img_url)

        user.profile_image.save(image[0], image[1], save=True)

        Wallet.objects.create(user=user)

        return user
