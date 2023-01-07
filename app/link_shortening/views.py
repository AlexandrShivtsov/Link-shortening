from django.shortcuts import HttpResponseRedirect, render
from django.utils import timezone
from django.http import HttpResponse

from link_shortening.forms import LinksForm
from link_shortening.models import Links
from link_shortening.services import make_unique_token, make_url


def index(request):
    long_link_form = LinksForm()
    if request.method == 'POST':

        long_link = request.POST.get('long_link')
        time_to_delete = request.POST.get('time_to_delete')
    # TODO error massage

        will_delete = timezone.now() + timezone.timedelta(int(time_to_delete))  # вираховуємо дату видалення посилання

        if Links.objects.filter(long_link=long_link).exists():
            """Якщо посилання існаує, беремо скоречене посилання з бази данних та віддаємо користувачу"""

            instance_link = Links.objects.get(long_link=long_link)
            short_link = instance_link.short_link
            previous_time_to_delete = instance_link.time_to_delete

            if will_delete > previous_time_to_delete:
                """Якщо час до видалення у новому запиті більший ніж у існуючому, 
                оновлюємо час до видалення на пізніший термін"""

                instance_link.time_to_delete = will_delete
                instance_link.save(update_fields=['time_to_delete'])

            # return render(request, template_name='short_link.html', context={'short_link': short_link})
            return HttpResponse('This is your link: ' + short_link)

        else:
            unique_token = make_unique_token()
            url = make_url(unique_token)

            Links.objects.create(
                long_link=long_link,
                short_link=url,
                unique_token=unique_token,
                time_to_delete=will_delete,
            )

            # return render(request, template_name='short_link.html', context={'short_link': url})
            return HttpResponse('This is your link: ' + url)

    return render(request, template_name='index.html', context={'form': long_link_form})


def redirect_to_original_url(request, **kwargs):
    unique_token = kwargs.pop('unique_token')
    """отримує unique_token за допомогою якого занаходить оригінальне 
    посилання та перенаправляю на нього користувача"""
    link_object = Links.objects.get(unique_token=unique_token)

    original_url = link_object.long_link # отримуємо оригінальне посилання

    counter = link_object.amount + 1 # збільшуємо лічильник
    link_object.amount=counter # присвоюємо полю amount нове значення
    link_object.save(update_fields=['amount']) # зберігаємо оновлене поле amount

    return HttpResponseRedirect(original_url)
