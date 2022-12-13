import random
import string

from celery import shared_task

from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone

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
    link = reverse('i:link', kwargs={'unique_token': unique_token})
    url = settings.HTTP_SCHEMA + settings.DOMAIN + settings.PORT + link
    return url


@shared_task()
def delete_depricated_links():
    """Здійснює перевірку поточної дати, порівнює з датою коли посилання повинно бути бидалене, якощо вони (дати)
    співпадають або поточна дата більша за дату коли поислання повинно було бути видалене, видаляє посилання"""
    current_time = timezone.now()
    all_links = Links.objects.all()
    for link in all_links:
        if current_time >= link.time_to_delete:
            link.delete()
