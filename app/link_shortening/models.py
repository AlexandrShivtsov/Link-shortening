from django.db import models

# Create your models here.


class Links(models.Model):
    long_link = models.URLField(max_length=1000, verbose_name='Long link')
    time_to_delete = models.DateTimeField(verbose_name='Days to delete')
    short_link = models.URLField(max_length=30, verbose_name='Short link')
    unique_token = models.CharField(max_length=5, verbose_name='Unique token')
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
