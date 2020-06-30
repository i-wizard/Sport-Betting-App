import calendar
import os
import time
import random
from urllib.parse import urlparse

import requests
import urllib3
from django.core import mail
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.files.temp import NamedTemporaryFile
from .site_details import get_site_details

from .mailing import *


class Helper:
    SMS_API_KEY = get_site_details.get_sms_key()
    _int_possibility = '0123456789'
    _aphanum_possibiliy = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    def user_upload_file_name(self, instance, filename):
        ts = calendar.timegm(time.gmtime())
        ext = filename.split('.')[-1]
        filename = "%s/%s.%s" % (instance.id, ts, ext)
        return os.path.join('uploads/profile', filename)

    def slider_image_upload(self, instance, filename):
        ts = calendar.timegm(time.gmtime())
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (ts, ext)
        return os.path.join('uploads/sliders', filename)

    def token_gen(self, length=6, ext='int'):
        if ext == 'int':
            possibilities = self._int_possibility
        elif ext == 'alphanum':
            possibilities = self._aphanum_possibiliy
        token = ""
        token_length = length

        for i in range(0, token_length):
            math_random = random.random()
            if math_random < 1:
                math_random = random.uniform(0.1, 0.9)
            token += possibilities[round(math_random * len(possibilities))]

        return token.lower()


    def admin_send_mail(self, message_body='', subject='', email=''):
        message = render_to_string('mails/admin/custom_mail.html', {
            'message': message_body,
        })

        mail_subject = 'TopPlaySport - {}'.format(subject)
        to_email = email
        raw_message = strip_tags(message)
        from_email = 'TopPlaySport <info@topplaysport.com>'
        mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)

    def urls_image_upload(self, url):
        img_url = url
        name = urlparse(img_url).path.split('/')[-1]

        response = requests.get(img_url)
        if response.status_code == 200:
            return name, ContentFile(response.content)
        return ()


class WinnersSort:
    def amount_to_tens(self, amount):
        return amount * 10

    def search(self, name, arr, key):
        for idx, p in enumerate(arr):
            if p[0][key] == name:
                # print("IN TRUE")
                return [True, idx]


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        current_page = 1

        for i in self.page.paginator.page_range:
            if self.page.number == i:
                current_page = i

        return Response({
            'pagination': {
                'count': self.page.paginator.count,
                'per_page': 9,
                'total': self.page.paginator.num_pages,
                'from': self.page.paginator.page_range[0],
                'to': self.page.paginator.num_pages,
                'current_page': current_page,
                'last_page': self.page.paginator.num_pages,
            },
            'results': data,
        })
