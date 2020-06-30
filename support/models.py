from django.db import models


class Support(models.Model):
    username = models.CharField(max_length=120, error_messages={'blank': "Please enter fullname.",
                                                                "required": "Please enter your fullname"})
    email = models.CharField(max_length=120, error_messages={'blank': "Please enter your email address",
                                                             "required": "Please enter your email address"})
    phone = models.CharField(max_length=120, blank=True, error_messages={'blank': "Please enter your phone number",
                                                             "required": "Please enter your phone number"})
    message = models.TextField(error_messages={'blank': "Please state your issue",
                                               "required": "Please state your issue"})
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
