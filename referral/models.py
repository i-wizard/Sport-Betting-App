from django.db import models
from django.utils import timezone

from users.models import User


class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrer')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_user')
    is_settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
