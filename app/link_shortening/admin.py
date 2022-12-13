from django.contrib import admin

from link_shortening.models import Links


class LinksAdmin(admin.ModelAdmin):

    list_display = ('long_link',
                    'time_to_delete',
                    'created',
                    'short_link',
                    'unique_token',
                    )


admin.site.register(Links, LinksAdmin)
