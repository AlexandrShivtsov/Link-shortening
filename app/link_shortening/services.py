import random
import string

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
    link = reverse('lsh:link', kwargs={'unique_token': unique_token})
    url = settings.HTTP_SCHEMA + settings.DOMAIN + settings.PORT + link
    return url


def chek_existing_long_link(long_link: str) -> bool:
    """Перевіяє чи не існує в базі данних URL, який необхідно скоротити"""
    if Links.objects.filter(long_link=long_link).exists():
        return True


def return_existing_short_link(long_link: str) -> str:
    """Якщо посилання існаує, беремо скоречене посилання з бази данних та віддаємо користувачу"""
    instance_link = Links.objects.get(long_link=long_link)
    short_link = instance_link.short_link
    return short_link


def chek_time_to_delete_short_link(long_link: str, will_delete: str):
    """Якщо час до видалення у новому запиті більший ніж у існуючому, 
    оновлюємо час до видалення на пізніший термін"""
    instance_link = Links.objects.get(long_link=long_link)
    previous_time_to_delete = instance_link.time_to_delete
    if will_delete > previous_time_to_delete:
        instance_link.time_to_delete = will_delete
        instance_link.save(update_fields=['time_to_delete'])


def save_to_db_new_link(long_link, url, unique_token, will_delete):
    """зберігає у db оригінальне посилання, скорочене посилання, токен та дату коли посилання буде видалене"""
    Links.objects.create(
            long_link=long_link,
            short_link=url,
            unique_token=unique_token,
            time_to_delete=will_delete,
        )


def link_click_counter(unique_token: str) -> str:
    """рахує кількість переходів за скороченим посиланням"""
    link_object = Links.objects.get(unique_token=unique_token)
    original_url = link_object.long_link # отримуємо оригінальне посилання
    counter = link_object.amount + 1 # збільшуємо лічильник
    link_object.amount=counter # присвоюємо полю amount нове значення
    link_object.save(update_fields=['amount']) # зберігаємо оновлене поле amount
    return original_url