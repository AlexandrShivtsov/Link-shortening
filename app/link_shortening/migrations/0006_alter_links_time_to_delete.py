# Generated by Django 4.1.3 on 2022-11-28 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_shortening', '0005_alter_links_time_to_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='time_to_delete',
            field=models.DateTimeField(verbose_name='Days to delete'),
        ),
    ]
