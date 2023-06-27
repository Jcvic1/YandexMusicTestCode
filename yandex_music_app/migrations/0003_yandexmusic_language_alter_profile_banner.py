# Generated by Django 4.2.2 on 2023-06-12 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_music_app', '0002_profile_banner_profile_follow_profile_thought'),
    ]

    operations = [
        migrations.AddField(
            model_name='yandexmusic',
            name='language',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='banner',
            field=models.ImageField(default='banner.avif', upload_to='banner_pictures'),
        ),
    ]
