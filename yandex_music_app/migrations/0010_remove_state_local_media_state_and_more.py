# Generated by Django 4.2.2 on 2023-06-21 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_music_app', '0009_alter_track_current_stations_origin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='state',
            name='local_media_state',
        ),
        migrations.AddField(
            model_name='track',
            name='station_settings2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
