import random
import string

from django.conf import settings
from django.shortcuts import reverse

from link_shortening.models import Links


def make_unique_token() -> str:
    """Створює унікальний токен, перевіряє чи не існкє такого токена у базі данних,
    даний токен є ключем до оригінального посиалання"""
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        unique_token = random.choices(letters, k=5)
        unique_token = ''.join(unique_token)

        if Links.objects.filter(unique_token=unique_token).exists():
            return make_unique_token()

        return unique_token


def make_url(unique_token: str) -> str:
    """На основі унікального токена,створює коротке посилання"""
    link = reverse('link', kwargs={'unique_token': unique_token})
    url = settings.HTTP_SCHEMA + settings.DOMAIN + settings.PORT + link
    return url