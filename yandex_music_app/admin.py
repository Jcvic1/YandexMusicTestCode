from django.contrib import admin
from .models import Profile, YandexMusic, YandexMusicTrack, State, Track, RadioHistoryState, Media

# Register your models here.

admin.site.register(Profile)
admin.site.register(YandexMusic)
admin.site.register(YandexMusicTrack)
admin.site.register(Media)
admin.site.register(State)
admin.site.register(Track)
admin.site.register(RadioHistoryState)
