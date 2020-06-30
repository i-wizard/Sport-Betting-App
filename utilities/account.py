from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.utils.html import strip_tags
from django.core import mail


def password_reset_link(request, user):
    current_site = get_current_site(request)
    message = render_to_string('mails/auth/password_reset.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': password_reset_token.make_token(user),
    })

    mail_subject = 'Password Reset Request'
    to_email = user.email
    raw_message = strip_tags(message)
    from_email = 'TopPlaySports <info@topplaysports.com>'
    # print(raw_message)
    mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)


class ResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


password_reset_token = ResetTokenGenerator()
