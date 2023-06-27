import os
from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, null=True, related_name='profile', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(
        upload_to='profile_pictures', default='blank-profile-picture.png')
    banner = models.ImageField(
        upload_to='banner_pictures', default='banner.jpg')
    thought = models.TextField(blank=True)
    follow = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name='follower')

    def __str__(self):
        return f"({self.user})"


class YandexMusic(models.Model):
    profile = models.ForeignKey(
        Profile, related_name='yandex_token', null=True, on_delete=models.CASCADE)
    yandex_token = encrypt(models.CharField(
        max_length=200, blank=True, null=True))
    language = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"({self.profile})"


class State(models.Model):
    profile = models.ForeignKey(
        Profile, related_name='states', null=True, on_delete=models.CASCADE)
    followers_only = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.profile})"


class YandexMusicTrack(models.Model):
    profile = models.ForeignKey(
        Profile, related_name='yandex_music_tracks', null=True, on_delete=models.CASCADE)
    track_id = models.CharField('track_id', max_length=40, null=True)
    track_name = models.CharField('track_name', max_length=100, null=True)
    track_artists = models.CharField(
        'track_artists', max_length=100, null=True)
    explicit_state = models.CharField('explicit', max_length=10, null=True)
    avatar_url = models.URLField('avatar', max_length=400, null=True)
    last_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.profile})"


class Media(models.Model):
    profile = models.ForeignKey(
        Profile, related_name='media_link', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    suffix = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"({self.profile})"


class Track(models.Model):
    profile = models.ForeignKey(
        Profile, related_name='last_track', null=True, on_delete=models.CASCADE)
    last_track = models.CharField(max_length=30, null=True, blank=True)
    tag_id = models.CharField(max_length=30, null=True, blank=True)
    tag = models.CharField(max_length=50, null=True, blank=True)
    sub_tag = models.CharField(max_length=50, null=True, blank=True)
    track_type = models.CharField(max_length=50, null=True, blank=True)
    track_type_id = models.CharField(max_length=50, null=True, blank=True)
    radio_first_track = models.CharField(max_length=50, null=True, blank=True)
    radio_set = models.CharField(max_length=50, null=True, blank=True)
    stations_origin = models.CharField(max_length=50, null=True, blank=True)
    station_settings2 = models.CharField(max_length=50, null=True, blank=True)
    current_stations_origin = models.CharField(
        max_length=50, null=True, blank=True)
    station_id_for_from = models.CharField(
        max_length=50, null=True, blank=True)

    def __str__(self):
        return f"({self.profile})"


class RadioHistoryState(models.Model):
    profile = models.ForeignKey(
        Profile, related_name='radio_history', null=True, on_delete=models.CASCADE)
    radio_history = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"({self.profile})"

  
