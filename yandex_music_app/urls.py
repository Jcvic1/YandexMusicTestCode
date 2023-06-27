from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('home', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('music', views.music, name='music'),
    path('people', views.people, name='people'),
    path('search_profile', views.search_profile, name='search_profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('follow/<id>', views.follow, name='follow'),
    path('page/<page_id>', views.page, name='page'),
    path('profile_status', views.profile_status, name='profile_status'),
    path('about_page_follow/<page_id>',views.about_page_follow, name='about_page_follow'),
    path('recover_profile', views.recover_profile, name='recover_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('add_media', views.add_media, name='add_media'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="yandex_music_app/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='yandex_music_app/password_reset_done.html'), name='password_reset_complete'),
    path('deactivate_profile', views.deactivate_profile, name='deactivate_profile'),
    path('delete_account', views.delete_account, name='delete_account'),
    path('yandex_music_login', views.yandex_music_login, name='yandex_music_login'),
    path('delete_yandex_music', views.delete_yandex_music, name='delete_yandex_music'),
    path('yandex_music_search_result/<page>' , views.yandex_music_search_result, name='yandex_music_search_result'),
    path('update_best/<searched>/<page>' , views.update_best, name='update_best'),
    path('update_tracks/<searched>/<page>' , views.update_tracks, name='update_tracks'),
    path('update_albums/<searched>/<page>' , views.update_albums, name='update_albums'),
    path('update_artists/<searched>/<page>' , views.update_artists, name='update_artists'),
    path('update_playlists/<searched>/<page>' , views.update_playlists, name='update_playlists'),
    path('update_podcasts/<searched>/<page>' , views.update_podcasts, name='update_podcasts'),
    path('update_podcast_episodes/<searched>/<page>' , views.update_podcast_episodes, name='update_podcast_episodes'),
    path('update_videos/<searched>/<page>' , views.update_videos, name='update_videos'),
    path('track/<id>' , views.track, name='track'),
    path('album/<id>' , views.album, name='album'),
    path('artist/<id>/<page>' , views.artist, name='artist'),
    path('update_artist_tracks/<id>/<page>' , views.update_artist_tracks, name='update_artist_tracks'),
    path('update_artist_albums/<id>/<page>' , views.update_artist_albums, name='update_artist_albums'),
    path('playlist/<uid>/<kind>' , views.playlist, name='playlist'),
    path('podcast/<id>' , views.podcast, name='podcast'),
    path('episode/<id>' , views.episode, name='episode'),
    path('video/<id>' , views.video, name='video'),
    path('suggestion_yandex_music_search_result',  views.suggestion_yandex_music_search_result,name='suggestion_yandex_music_search_result'),
    path('yandex_music_client' , views.yandex_music_client, name='yandex_music_client'),
    path('yandex_radio' , views.yandex_radio, name='yandex_radio'),
    path('new_releases' , views.new_releases, name='new_releases'),
    path('charts' , views.charts, name='charts'),
    path('new_playlists' , views.new_playlists, name='new_playlists'),
    path('mixes' , views.mixes, name='mixes'),
    path('client_tracks' , views.client_tracks, name='client_tracks'),
    path('client_playlists' , views.client_playlists, name='client_playlists'),
    path('client_albums' , views.client_albums, name='client_albums'),
    path('client_artists' , views.client_artists, name='client_artists'),
    path('client_podcasts' , views.client_podcasts, name='client_podcasts'),
    path('favourite', views.favourite,name='favourite'),
    path('tag/<tag_id>', views.tag,name='tag'),
    path('promotion/<path:promotion_url>', views.promotion,name='promotion'),
    path('toggle_like', views.toggle_like,name='toggle_like'),
    path('toggle_visibility', views.toggle_visibility,name='toggle_visibility'),
    path('to_album/<id>', views.to_album,name='to_album'),
    path('lyrics/<id>', views.lyrics,name='lyrics'),
    path('to_artist/<id>', views.to_artist,name='to_artist'),
    path('add_tracks/<id>', views.add_tracks,name='add_tracks'),
    path('collections', views.collections,name='collections'),
  
]