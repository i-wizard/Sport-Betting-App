from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Mailer:
    def notify_balance(self, amount, username):
        amount = amount/100
        message = render_to_string('mails/admin/insufficient_fund_alert.html', {'amount': amount, 'username': username})
        subject = 'Topplaysport Insufficient funds'

        mail_subject = subject
        to_email = 'confiyobo@gmail.com'
        raw_message = strip_tags(message)
        from_email = 'Topplaysport <noreply@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def send_first_time_mail(self, email, username):
        message = render_to_string('mails/auth/register_success.html', {'username': username})
        subject = 'David from Topplaysport Checking in'

        mail_subject = subject
        to_email = email
        raw_message = strip_tags(message)
        from_email = 'Topplaysport <noreply@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def send_winning_msg(self, user):
        message = render_to_string('mails/bets/win.html')
        subject = 'YOU ARE A WINNER'

        mail_subject = 'Topplaysport - {}'.format(subject)
        to_email = user.email
        raw_message = strip_tags(message)
        from_email = 'Topplaysport <info@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def send_my_mail(self, amount):
        message = render_to_string('mails/bets/test.html', {'amount':amount})
        subject = 'TESTING AMOUNT DISBURSED'

        mail_subject = 'Topplaysport - {}'.format(subject)
        to_email = 'confiyobo@gmail.com'
        raw_message = strip_tags(message)
        from_email = 'Topplaysport <info@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def send_referrer_msg(self, user, username):
        message = render_to_string('mails/referrals/referee.html', {'username': username})
        subject = 'New Referral Notification'

        mail_subject = 'Topplaysport - {}'.format(subject)
        to_email = user.email
        raw_message = strip_tags(message)
        from_email = 'Topplaysport <info@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def send_referrer_winner(self, user, username):
        message = render_to_string('mails/referrals/referral_paid.html', {'username': username})
        subject = 'Referral Notification'

        mail_subject = 'Topplaysport - {}'.format(subject)
        to_email = user.email
        raw_message = strip_tags(message)
        from_email = 'Topplaysport <info@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def send_raffle_player(self, user, raffle_id):
        message = render_to_string('mails/raffle/qualification.html', {'username': user.username, 'raffle_id': raffle_id})
        subject = 'Raffle Draw Added'

        mail_subject = 'Topplaysport - {}'.format(subject)
        to_email = user.email
        raw_message = strip_tags(message)
        from_email = 'Topplaysport <info@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def send_raffle_winner(self, user):
        message = render_to_string('mails/raffle/won.html', {'username': user.username})
        subject = 'You Are A Winner'

        mail_subject = 'Topplaysport - {}'.format(subject)
        to_email = user.email
        raw_message = strip_tags(message)
        from_email = 'Topplaysport <info@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def send_support_message(self, username):
        message = render_to_string('mails/support.html', {'username': username})
        subject = 'New message from users'

        mail_subject = 'Topplaysport - {}'.format(subject)
        to_email = 'info@topplaysport.com'
        raw_message = strip_tags(message)
        from_email = 'Topplaysport <info@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def admin_response(self, message, email, name):
        message = render_to_string('mails/admin/support_response.html', {
            'message': message, 'name': name
        })

        mail_subject = 'Topplaysport - Support Response'
        to_email = email
        raw_message = strip_tags(message)
        from_email = 'TopPlaySport <info@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def admin_message(self, message, email, title):
        message = render_to_string('mails/admin/custom_mail.html', {
            'message': message
        })

        mail_subject = f'Topplaysport - {title}'
        to_email = email
        raw_message = strip_tags(message)
        from_email = 'TopPlaySport <info@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)
