# Generated by Django 4.2.2 on 2023-06-15 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_music_app', '0005_remove_state_stream_state_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RadioHistory',
            new_name='RadioHistoryState',
        ),
        migrations.RenameModel(
            old_name='Tracks',
            new_name='Track',
        ),
        migrations.RenameModel(
            old_name='YandexMusicTracks',
            new_name='YandexMusicTrack',
        ),
    ]
