from api.serializers import LinksSerializers

from link_shortening.models import Links

from rest_framework import generics
from rest_framework.response import Response


class LinksAPIView(generics.CreateAPIView):

    def post(self, request):
        """За допомогою оригінального посилання проводиться перевірка чи існує таке посилання в базі данних, якщо ні,
        ствроює нове коротке посилання та повертає клієнут разом з датою коли його буду видалено"""

        serializers = LinksSerializers(data=request.data)
        serializers.is_valid()
        long_link = serializers.validated_data['long_link']
        link_instance = Links.objects.filter(long_link=long_link)
        if link_instance.exists():
            return Response({'short_link': link_instance[0].short_link})

        serializers.save()
        return Response({'short_link': link_instance[0].short_link})
