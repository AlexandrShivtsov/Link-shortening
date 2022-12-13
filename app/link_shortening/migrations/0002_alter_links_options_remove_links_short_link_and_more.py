# Generated by Django 4.1.3 on 2022-11-26 16:43
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_shortening', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='links',
            options={'verbose_name': 'Long link', 'verbose_name_plural': 'long links'},
        ),
        migrations.RemoveField(
            model_name='links',
            name='short_link',
        ),
        migrations.AddField(
            model_name='links',
            name='time_to_delete',
            field=models.IntegerField(default=1, verbose_name='Time to delete'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='links',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Short_links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_link', models.URLField(max_length=10, verbose_name='Short link')),
                ('created', models.DateField(auto_now_add=True)),
                ('unique_token', models.CharField(max_length=5, verbose_name='Unique token')),
                ('original_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                    related_name='original_link', to='link_shortening.links',
                                                    verbose_name='Long link')),
            ],
            options={
                'verbose_name': 'Short link',
                'verbose_name_plural': 'Short links',
            },
        ),
    ]
