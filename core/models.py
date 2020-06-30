from django.db import models

from utilities.helper import Helper


class Slider(models.Model):
    image = models.ImageField(upload_to=Helper().slider_image_upload)
    should_show = models.BooleanField(default=False)


class GameSetting(models.Model):
    num_smart_users = models.SmallIntegerField(default=5)
    min_user_limit = models.SmallIntegerField(default=600)
    num_jackpot_winners = models.SmallIntegerField(default=5)
    trial_ending = models.DateField(null=True, blank=True)
