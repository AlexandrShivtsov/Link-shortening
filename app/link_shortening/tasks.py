from celery import shared_task

from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone

from link_shortening.models import Links


@shared_task()
def delete_depricated_links():
    """Здійснює перевірку поточної дати, порівнює з датою коли посилання повинно бути бидалене, якощо вони (дати)
    співпадають або поточна дата більша за дату коли поислання повинно було бути видалене, видаляє посилання"""
    current_time = timezone.now()
    all_links = Links.objects.all()
    for link in all_links:
        if current_time >= link.time_to_delete:
            link.delete()
