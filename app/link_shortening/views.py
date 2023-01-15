from django.shortcuts import HttpResponseRedirect, render
from django.utils import timezone
from django.http import HttpResponse

from link_shortening.forms import LinksForm
from link_shortening.models import Links
from link_shortening.services import (make_unique_token, make_url, chek_existing_long_link, 
                                        return_existing_short_link, chek_time_to_delete_short_link, 
                                        save_to_db_new_link, link_click_counter)


def index(request): 
    long_link_form = LinksForm()
    if request.method == 'POST':

        long_link = request.POST.get('long_link')
        time_to_delete = request.POST.get('time_to_delete')
    # TODO error massage

        will_delete = timezone.now() + timezone.timedelta(int(time_to_delete))  # вираховуємо дату видалення посилання
        
        if chek_existing_long_link(long_link):
            short_link = return_existing_short_link(long_link=long_link)
            chek_time_to_delete_short_link(long_link=long_link, will_delete=will_delete)

            return HttpResponse('This is your link: ' + short_link)

        else:
            unique_token = make_unique_token()
            url = make_url(unique_token)
            save_to_db_new_link(long_link, url, unique_token, will_delete)

            return HttpResponse('This is your link: ' + url)

    return render(request, template_name='index.html', context={'form': long_link_form})


def redirect_to_original_url(request, **kwargs):
    """з url отримує unique_token за допомогою якого занаходить оригінальне 
    посилання та перенаправляю на нього користувача"""
    unique_token = kwargs.pop('unique_token')
    original_url = link_click_counter(unique_token=unique_token)
    return HttpResponseRedirect(original_url)
