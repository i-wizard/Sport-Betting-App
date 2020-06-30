from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from utilities.helper import Helper


class UserManager(BaseUserManager):
    def _create_user(self, phone, calling_code, **extra_fields):
        user = self.model(phone=phone, calling_code=calling_code, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password.lowe(), **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password.lower())
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    profile_image = models.ImageField(upload_to=Helper().user_upload_file_name, default='uploads/profile/no-img.png')
    username = models.CharField(_("Username"), unique=True, max_length=100, null=True,
                                error_messages={'blank': "Please enter username."})
    email = models.EmailField(max_length=40, unique=True, null=True,
                              error_messages={'required': 'Please provide email address.',
                                              'unique': 'A user with this email address already exist.'})
    phone = models.CharField(max_length=20, unique=True,
                             error_messages={'required': 'Please provide your phone number.',
                                             'unique': 'A user with this phone number already exist.'})
    calling_code = models.IntegerField(default=234)
    referral_code = models.CharField(max_length=30, blank=True, null=True)
    referred = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'email', 'calling_code']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return '{} - {}'.format(self.username, self.pk)

