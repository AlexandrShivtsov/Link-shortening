# Generated by Django 4.1.3 on 2022-12-24 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_shortening', '0008_coanter'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='amount',
            field=models.IntegerField(default=1, verbose_name='amount of visiting link'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Coanter',
        ),
    ]
