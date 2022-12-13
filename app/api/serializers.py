from django.utils import timezone

from link_shortening.models import Links
from link_shortening.tasks import make_unique_token, make_url

from rest_framework import serializers


class LinksSerializers(serializers.Serializer):
    long_link = serializers.CharField(max_length=2083)
    time_to_delete = serializers.CharField(max_length=2)

    def create(self, validated_data):
        """Отримує оригінальне посилання та час до видалення скороченого посилання, створює коротке посилання"""
        long_link = validated_data['long_link']
        time_to_delete = validated_data['time_to_delete']
        unique_token = make_unique_token()
        url = make_url(unique_token)
        will_delete = timezone.now() + timezone.timedelta(int(time_to_delete))

        return Links.objects.create(
            long_link=long_link,
            short_link=url,
            unique_token=unique_token,
            time_to_delete=will_delete,
        )
