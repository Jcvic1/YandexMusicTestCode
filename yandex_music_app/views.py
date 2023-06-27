import os
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from .models import Profile, State, Track, RadioHistoryState, YandexMusic, YandexMusicTrack, Media
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django import template
from math import floor
from random import random
from .radio import Radio
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from yandex_music import Client
import json
import requests
import dotenv
from functools import wraps
# Create your views here.



def custom_login_required():
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                response = HttpResponse(status=401)
                response['HX-Redirect'] = 'login_user'
                return response
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


# PROFILE

# Create your views here.
def landing(request):
    if not request.user.is_authenticated:
        return redirect ('login_user')
    return redirect ('home')

@custom_login_required()
def home(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    profiles = Profile.objects.all().exclude(user=user)
    profile.last_seen = datetime.now()
    profile.save()
    followers = profile.follower.all()
    existing_token = YandexMusic.objects.filter(profile=profile)
    return render(request, "yandex_music_app/home.html", {'profile': profile, 'profiles': profiles, 'followers': followers, 'existing_token': existing_token})


@custom_login_required()
def profile(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    profiles = Profile.objects.all().exclude(user=user)
    profile.last_seen = datetime.now()
    profile.save()
    followers = profile.follower.all()
    existing_token = YandexMusic.objects.filter(profile=profile)
    from_ = 'profile'
    return render(request, "yandex_music_app/profile.html", {'profile': profile, 'profiles': profiles, 'followers': followers, 'existing_token': existing_token, 'from_': from_})


@custom_login_required()
def music(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    profiles = Profile.objects.all().exclude(user=user)
    profile.last_seen = datetime.now()
    profile.save()
    followers = profile.follower.all()
    existing_token = YandexMusic.objects.filter(profile=profile)
    return render(request, "yandex_music_app/music.html", {'profile': profile, 'profiles': profiles, 'followers': followers, 'existing_token': existing_token})


@custom_login_required()
def people(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    profiles = Profile.objects.all().exclude(user=user)
    profile.last_seen = datetime.now()
    profile.save()
    followers = profile.follower.all()
    existing_token = YandexMusic.objects.filter(profile=profile)
    return render(request, "yandex_music_app/people_.html", {'profile': profile, 'profiles': profiles, 'followers': followers, 'existing_token': existing_token})



@custom_login_required()
def page(request, page_id):
    from_ = request.GET.get('from')
    profile = Profile.objects.get(id=page_id)
    user_profile = Profile.objects.get(user=request.user)
    followers = profile.follower.all()
    return render(request, "yandex_music_app/about_me.html", {'profile': profile, 'followers': followers, 'user_profile': user_profile, 'from_': from_})


@custom_login_required()
def about_page_follow(request, page_id):
    if request.method == 'POST':
        from_ = request.GET.get('from')
        profile = Profile.objects.get(id=page_id)
        user_profile = Profile.objects.get(user=request.user)
        follow = user_profile.follow.all()
        followers = profile.follower.all()
        if profile in follow:
            user_profile.follow.remove(profile)
        else:
            user_profile.follow.add(profile)
        return render(request, "yandex_music_app/about_me.html", {'profile': profile, 'followers': followers, 'user_profile': user_profile, 'from_': from_})
    return render(request, "yandex_music_app/page_follow.html", {'profile': profile, 'follow': follow, 'followers': followers, 'user_profile': user_profile, 'from_': from_})


@custom_login_required()
def follow(request, id):
    if request.method == 'POST':
        tag = request.POST.get('tag')
        tag_type =  request.POST.get('tag_type')
        from_ = request.POST.get('from')
        user = User.objects.get(id=request.user.id)
        user_profile = Profile.objects.get(id=id)
        profile = Profile.objects.get(user=request.user)
        profiles = Profile.objects.all().exclude(user=user)
        follow = profile.follow.all()
        followers = profile.follower.all()
        if user_profile in follow:
            profile.follow.remove(user_profile)
           
        else:
            profile.follow.add(user_profile)
           
        return render(request, "yandex_music_app/people.html", {'profile': profile, 'profiles': profiles, 'user_profile': user_profile, 'follow': follow, 'followers': followers, 'tag': tag, 'tag_type': tag_type, 'from_': from_})
    return render(request, "yandex_music_app/people.html", {'profile': profile, 'profiles': profiles, 'user_profile': user_profile, 'follow': follow, 'followers': followers, 'tag': tag, 'tag_type': tag_type, 'from_': from_})


@custom_login_required()
def profile_status(request):
    profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=request.user)
    followers_only = State.objects.get(profile_id = profile.id)
    if followers_only.followers_only is False:
        followers_only.followers_only = True
        followers_only.save()
        messages.warning(request, ("Profile Private!"))
        return redirect('profile')
    if followers_only.followers_only is True:
        followers_only.followers_only = False            
        followers_only.save()
        messages.warning(request, ("Profile Public!"))
        return redirect('profile')       
    return render(request, "yandex_music_app/profile.html", {'profile': profile, 'user_profile': user_profile})


@custom_login_required()
def add_media(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        twitter = request.POST['twitter']
        vk = request.POST['vk']
        facebook = request.POST['facebook']
        instagram = request.POST['instagram']

        media_items = Media.objects.filter(profile=profile)
        for media_item in media_items:
            if media_item.name == 'twitter':
                media_item.suffix = twitter
            elif media_item.name == 'vk':
                media_item.suffix = vk
            elif media_item.name == 'facebook':
                media_item.suffix = facebook
            elif media_item.name == 'instagram':
                media_item.suffix = instagram            
            
            media_item.save()

        messages.success(request, ("Media Saved!"))
        return redirect('edit_profile')   




def search_profile(request):
    if request.method == "POST":
        searched = request.POST['searched']
        tag = request.GET.get('tag')
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        profile_lists = Profile.objects.filter(
            user__username__contains=searched).exclude(user=request.user)
        if searched is not None:
            searched = searched.replace('#', '')
            searched = searched.strip()
            if not searched:
                messages.error(request, ("No Search Query!"))
                return render(request,
                              "yandex_music_app/msg.html")
            if not profile_lists:
                messages.error(request, ("Profile Does Not Exist!"))
                return render(request,
                              "yandex_music_app/msg.html")

            else:
                return render(request,
                              "yandex_music_app/profile_search.html",
                              {'searched': searched,
                               'profile_lists': profile_lists, 'profile': profile, 'tag': tag})
    else:
        return render(request,
                      "yandex_music_app/profile_search.html")


@custom_login_required()
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('profile_pic') is None and request.FILES.get('banner') is not None:
            profile_pic = profile.profile_pic
            banner = request.FILES['banner']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            thought = request.POST['thought']

            file_name = banner.name
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            if not any(file_name.lower().endswith(ext) for ext in allowed_extensions):
                messages.error(request, ("Try jpg, jpeg or png, Image Type Not Accepted! "))
                return redirect('edit_profile')
            else:
                profile.banner.delete()
                profile.save()
                profile.banner = banner
                profile.profile_pic = profile_pic
                profile.user.first_name = first_name
                profile.user.last_name = last_name
                profile.user.email = email
                profile.thought = thought
                profile.save()
                profile.user.save()

                messages.success(request, ("Profile Update Successful!"))
                return redirect('edit_profile')

        if request.FILES.get('banner') is None and request.FILES.get('profile_pic') is not None:
            banner = profile.banner
            profile_pic = request.FILES['profile_pic']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            thought = request.POST['thought']


            file_name = profile_pic.name
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            if not any(file_name.lower().endswith(ext) for ext in allowed_extensions):
                messages.error(request, ("Try jpg, jpeg or png, Image Type Not Accepted! "))
                return redirect('edit_profile')
            else:
                profile.profile_pic.delete()
                profile.save()
                profile.profile_pic = profile_pic
                profile.banner = banner
                profile.user.first_name = first_name
                profile.user.last_name = last_name
                profile.user.email = email
                profile.thought = thought
                profile.save()
                profile.user.save()

                messages.success(request, ("Profile Update Successful!"))
                return redirect('edit_profile')

        if request.FILES.get('banner') is None and request.FILES.get('profile_pic') is None:
            banner = profile.banner
            profile_pic = profile.profile_pic
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            thought = request.POST['thought']

            profile.profile_pic = profile_pic
            profile.banner = banner
            profile.user.first_name = first_name
            profile.user.last_name = last_name
            profile.user.email = email
            profile.thought = thought
            profile.save()
            profile.user.save()

            messages.success(request, ("Profile Update Successful!"))
            return redirect('edit_profile')

        if request.FILES.get('banner') is not None and request.FILES.get('profile_pic') is not None:
            banner = request.FILES['banner']
            profile_pic = request.FILES['profile_pic']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            thought = request.POST['thought']


            file_name_banner = banner.name
            file_name_profile_pic = profile_pic.name
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            if not any(file_name_banner.lower().endswith(ext) for ext in allowed_extensions) or not any(file_name_profile_pic.lower().endswith(ext) for ext in allowed_extensions):
                messages.error(request, ("Try jpg, jpeg or png, Image Type Not Accepted! "))
                return redirect('edit_profile')
            else:
                profile.profile_pic.delete()
                profile.banner.delete()
                profile.save()
                profile.profile_pic = profile_pic
                profile.banner = banner
                profile.user.first_name = first_name
                profile.user.last_name = last_name
                profile.user.email = email
                profile.thought = thought
                profile.save()
                profile.user.save()

                messages.success(request, ("Profile Update Successful!"))
                return redirect('edit_profile')

    return render(request, "yandex_music_app/update_profile.html", {'profile': profile})


@custom_login_required()
def deactivate_profile(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        logout(request)
        messages.success(request, ("Profile Deactivate Successful!"))
    return redirect("login_user")


@custom_login_required()
def delete_account(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        profile.user.delete()
        messages.success(request, ("Account Delete Successful!"))
    return redirect("login_user")


def recover_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.filter(username=username)
        if user.exists():
            for user in user:
                if user.is_active is True:
                    messages.error(
                        request, ("You Have Active Profile!"))
                else:
                    user.is_active = True
                    user.save()
                    messages.success(request, ("Profile Activate Successful!"))
                    return redirect('login_user')
        else:
            messages.error(request, ("You Don't Have A Profile!"))
    return render(request, "yandex_music_app/recover_profile.html")


@custom_login_required()
def change_password(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if not check_password(old_password, profile.user.password):
            old_pass = True
            return render(request, "yandex_music_app/update_password.html", {'profile': profile, 'old_pass': old_pass})
        elif check_password(old_password, profile.user.password) and new_password == confirm_password:
            profile.user.set_password(new_password)
            profile.user.save()
            messages.success(request, ("Password Update Successful!"))
            return redirect("login_user")
        else:
            new_pass = True
            return render(request, "yandex_music_app/update_password.html", {'profile': profile, 'new_pass': new_pass})
    return render(request, "yandex_music_app/update_password.html", {'profile': profile})


def reset_password(request):
    if request.method == "POST":
        data = request.POST['email']
        associated_users = User.objects.filter(Q(email=data))
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                plaintext = template.loader.get_template(
                    'yandex_music_app/email.txt')
                htmltemp = template.loader.get_template(
                    'yandex_music_app/email_text.html')
                content = {
                    "email": user.email,
                    'domain': '6534-46-31-25-109.ngrok-free.app',
                    'site_name': 'YMgroup',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https',
                }
                text_content = plaintext.render(content)
                html_content = htmltemp.render(content)
                try:
                    msg = EmailMultiAlternatives(subject, text_content, 'Website <ymgroup.com>', [user.email], headers={'Reply-To': 'ymgroup.mailing.com'})
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(
                    request, 'Reset Link Sent, Check Email!')
                return redirect("login_user")
        else:
            messages.error(request, 'Invalid Email Sent, Check Email!')
    return render(request, "yandex_music_app/reset_password.html")


# YANDEX MUSIC


# ---------------------------------------------AUTHOURIZATION-----------------------------------------------




@custom_login_required()
def yandex_music_login(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        get_token = request.POST.get('token')
        language = request.POST.get('language')
        if 'checked' in request.POST and request.POST['checked'] == 'on':
            try:
                client = Client(get_token).init()
            except Exception:
                messages.error(request, ("Token Couldn't Be verified!"))
                return redirect("music")    
            else:
                ym_token = get_token
                existing_token = YandexMusic.objects.filter(profile=profile)
                if existing_token:
                    existing_token.delete()
                    YandexMusic.objects.create(profile=profile, yandex_token=ym_token, language=language)
                    messages.success(request, ("Account Access Updated"))
                    return redirect("music")
                else:
                    YandexMusic.objects.create(profile=profile, yandex_token=ym_token, language=language)
                    messages.success(request, ("Account Access Granted"))
                    return redirect("music")

        messages.error(request, ("Agree To Terms!"))
        return redirect("music")
    return redirect("music")

@custom_login_required()
def delete_yandex_music(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            token = YandexMusic.objects.get(profile=profile)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return redirect("music")
        else:
            token.delete()
            messages.warning(request, ("Account Removed!"))
            return redirect("music")
    

# --------------------------------------------------LANDING------------------------------------------------------





@custom_login_required()
def yandex_music_client(request):
    if request.method == 'POST':
        client_error = True
        try:
            profile = Profile.objects.get(user=request.user)
            
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html", {'client_error': client_error})
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html", {'client_error': client_error})
            else:
                try:
                    profile.last_seen = datetime.now()
                    profile.save()
                    client = Client(token=token, language=language).init()
                    user_client = client.me
                    
                    home = client.landing(['personalplaylists', 'promotions', 'new-releases', 'new-playlists', 'chart', 'mixes', 'artists', 'albums', 'playlists', 'play_contexts'])
                 
                    for block in home.blocks:
                        if block.type == 'personal-playlists':
                            block_personal_playlists = block.entities
                        elif block.type == 'promotions':
                            block_promotions = block.entities
                        elif block.type == 'new-releases':
                            block_new_releases = block.entities
                        elif block.type == 'new-playlists':
                            block_new_playlists = block.entities
                        elif block.type == 'mixes':
                            block_mixes = block.entities
                        elif block.type == 'chart':
                            block_chart = block.entities
                        elif block.type == 'artists':
                            block_artists = block.entities
                        elif block.type == 'albums':
                            block_albums = block.entities
                        elif block.type == 'playlists':
                            block_playlists = block.entities
                        elif block.type == 'play_contexts':
                            block_play_contexts = block.entities
                        else:
                            pass
                    
                    
                        
                    # podcasts = client.podcasts()
                    # podcasts_ids = []
                    
                    # for id in podcasts.podcasts:
                    #     podcasts_ids.append(id)
                    # podcasts_album = client.albums(podcasts_ids)
                    


                    # tracks = []
                    # episode_tracks = []
                    # albums = []
                    # podcast_albums = []
                    # tracks_ = client.users_likes_tracks().fetch_tracks()
                    # for track in tracks_:
                    #     if 'podcast' not in track.type:
                    #         tracks.append(track)
                    #     else:
                    #         episode_tracks.append(track)
                    # albums_ = client.users_likes_albums()
                    # for album in albums_:
                    #     if  album.album.type != 'podcast':
                    #         albums.append(album.album)
                    #     else:
                    #         podcast_albums.append(album.album)
                    # artists = client.users_likes_artists()
                    # playlists = client.users_likes_playlists()
                    # user_playlists = client.users_playlists_list()
                   
                    fav_tracks = []
                    tracks_ = client.users_likes_tracks().fetch_tracks()
                    for track in tracks_:
                            fav_tracks.append(track.id)    

                    context = {'home': home, 'fav_tracks': fav_tracks, 'block_personal_playlists': block_personal_playlists, 'block_promotions': block_promotions, 'block_new_releases': block_new_releases, 'block_chart': block_chart, 'block_mixes': block_mixes, 'block_new_playlists': block_new_playlists,'user_client': user_client}
                except Exception:
                    messages.error(request, ("Verify Yandex Account Has Subscription!"))
                    return render(request, "yandex_music_app/yandex_client.html") 

        return render(request, "yandex_music_app/yandex_client.html", context)




@custom_login_required()
def yandex_radio(request):
    if request.method == 'POST':
        set_up = request.POST.get('set_up')
        personal_stations = request.POST.get('personal_stations')
        settings2 = request.POST.get('settings2')
        station_id_type = request.POST.get('station_id_type')
        station_id_tag = request.POST.get('station_id_tag')
        mood_energy = request.POST.get('mood_energy')
        diversity = request.POST.get('diversity')
        lang_ = request.POST.get('language')
        reset = request.POST.get('reset')
        reset_mood_energy = request.POST.get('reset_mood_energy')
        reset_diversity = request.POST.get('reset_diversity')
        reset_language = request.POST.get('reset_language')
        playing_station = request.POST.get('playing_station')

        client_error = True
        try:
            profile = Profile.objects.get(user=request.user)
            
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html", {'client_error': client_error})
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html", {'client_error': client_error})
            else:
                client = Client(token=token, language=language).init()
                personal_stations_list = None
                station_settings2 = None
                station = None
                
                if personal_stations:
                    personal_stations_ = client.rotor_stations_dashboard()
                    personal_stations_list = personal_stations_.stations

                elif settings2:
                    if reset:
                        mood_energy = reset_mood_energy
                        diversity = reset_diversity
                        lang_ = reset_language
                    station = f'{station_id_type}:{station_id_tag}'
            
                    station_settings2 = client.rotor_station_settings2(station=station, mood_energy=mood_energy, diversity=diversity, language=lang_)


                context = {'set_up': set_up, 'reset': reset, 'station': station, 'station_settings2': station_settings2, 'mood_energy': mood_energy, 'diversity': diversity, 'language': lang_, 'playing_station': playing_station, 'settings2': settings2, 'personal_stations_list': personal_stations_list, 'station_settings2': station_settings2}
                return render(request, "yandex_music_app/radio_track.html", context)
              


@custom_login_required()
def new_releases(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html")
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html")
            else:
                client = Client(token=token, language=language).init()
                new_releases_full = client.new_releases()
                new_releases_full_ids = []
                
                for id in new_releases_full.new_releases:
                    new_releases_full_ids.append(id)
                new_releases_full_album = client.albums(new_releases_full_ids)
                return render(request, "yandex_music_app/new_releases.html", {'new_releases_full': new_releases_full, 'new_releases_full_album': new_releases_full_album})



@custom_login_required()
def client_playlists(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html")
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html")
            else:
                client = Client(token=token, language=language).init()
                tracks = []
                tracks_ = client.users_likes_tracks().fetch_tracks()
                for track in tracks_:
                    if 'podcast' not in track.type:
                        tracks.append(track)
                playlists = client.users_likes_playlists()
                user_playlists = client.users_playlists_list()
                return render(request, "yandex_music_app/client_playlists.html", {'tracks': tracks, 'playlists': playlists, 'user_playlists': user_playlists})


@custom_login_required()
def client_tracks(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html")
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html")
            else:
                client = Client(token=token, language=language).init()
                tracks = []
                tracks_ = client.users_likes_tracks().fetch_tracks()
                for track in tracks_:
                    if 'podcast' not in track.type:
                        tracks.append(track)
                    
                return render(request, "yandex_music_app/client_tracks.html", {'tracks': tracks})



@custom_login_required()
def client_albums(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html")
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html")
            else:
                client = Client(token=token, language=language).init()
                albums = []
                albums_ = client.users_likes_albums()
                for album in albums_:
                    if  album.album.type != 'podcast':
                        albums.append(album.album)
                    
                return render(request, "yandex_music_app/client_albums.html", {'albums': albums})



@custom_login_required()
def client_artists(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html")
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html")
            else:
                client = Client(token=token, language=language).init()
                artists = client.users_likes_artists()
                return render(request, "yandex_music_app/client_artists.html", {'artists': artists})



@custom_login_required()
def client_podcasts(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html")
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html")
            else:
                client = Client(token=token, language=language).init()
                episode_tracks = []
                podcast_albums = []


                tracks_ = client.users_likes_tracks().fetch_tracks()
                for track in tracks_:
                    if 'podcast' in track.type:
                        episode_tracks.append(track)

                albums_ = client.users_likes_albums()
                for album in albums_:
                    if  album.album.type == 'podcast':
                        podcast_albums.append(album.album)        
                            
                return render(request, "yandex_music_app/client_podcasts.html", {'episode_tracks': episode_tracks, 'podcast_albums': podcast_albums})



@custom_login_required()
def charts(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html")
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html")
            else:
                client = Client(token=token, language=language).init()
                chart_full = client.chart('world')
                chart_full_tracks = chart_full.chart.tracks

                fav_tracks = []
                tracks_ = client.users_likes_tracks().fetch_tracks()
                for track in tracks_:
                        fav_tracks.append(track.id)
                return render(request, "yandex_music_app/charts.html", {'chart_full_tracks': chart_full_tracks, 'fav_tracks': fav_tracks})




@custom_login_required()
def new_playlists(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html")
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html")
            else:
                client = Client(token=token, language=language).init()
                new_playlists_full = []
                new_playlists_full_ = client.new_playlists()
                for new_playlist in new_playlists_full_.new_playlists:
                    playlist = client.users_playlists(new_playlist.kind, new_playlist.uid)
                    new_playlists_full .append(playlist)
                return render(request, "yandex_music_app/new_playlists.html", {'new_playlists_full_': new_playlists_full_, 'new_playlists_full': new_playlists_full})




@custom_login_required()
def mixes(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html")
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html")
            else:
                client = Client(token=token, language=language).init()
                mixes_ = client.landing('mixes')
                for block in mixes_.blocks:
                    mixes = block.entities
                genres = client.genres()
                return render(request, "yandex_music_app/mixes.html", {'mixes': mixes, 'genres': genres})



@custom_login_required()
def tag(request, tag_id):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Exception:
            messages.error(request, ("No Registered Account, Login In!"))
            return render(request, "yandex_music_app/msg.html")
        else:
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
                return render(request, "yandex_music_app/msg.html")
            else:
                client = Client(token=token, language=language).init()
                playlists = []
                mixes = client.tags(tag_id)
                for id in mixes.ids:
                    playlist = client.users_playlists(id.kind, id.uid)
                    playlists.append(playlist)
                return render(request, "yandex_music_app/tag.html", {'playlists': playlists, 'mixes': mixes})



@custom_login_required()
def promotion(request, promotion_url):
    if request.method == 'POST':
        album_data = None
        playlist_data = None
        tracks = []
        if 'album' in promotion_url:
            promotion_url = promotion_url.replace('album', 'albums')
            url = 'https://api.music.yandex.ru'+ promotion_url + '/with-tracks'
            headers = {'Accept-Language': 'en-US'}
            timeout = 120
            response = requests.get(url=url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                album_data = response.json()
                for i, volume in enumerate(album_data['result']['volumes']):
                    if len(album_data['result']['volumes']) > 1:
                        tracks.append(f'💿 Disc {i + 1}')
                    tracks += volume
            else:
                print(f"Request failed with status code {response.status_code}")
        elif 'playlists' in promotion_url:
            url = 'https://api.music.yandex.ru'+ promotion_url
            headers = {'Accept-Language': 'en-US'}
            timeout = 120
            response = requests.get(url=url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                playlist_data = response.json()
                
            else:
                print(f"Request failed with status code {response.status_code}")
              
        return render(request, "yandex_music_app/promotion.html", {'playlist_data': playlist_data, 'album_data': album_data, 'tracks': tracks})





# --------------------------------------------------SEARCH------------------------------------------------------        





@custom_login_required()
def yandex_music_search_result(request, page):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        try:
            token = YandexMusic.objects.get(profile=profile).yandex_token
            language = YandexMusic.objects.get(profile=profile).language
        except Exception:
            messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
            return render(request, "yandex_music_app/msg.html")

        else:    
            client = Client(token=token, language=language).init()
            
        if request.method == 'POST':
            searched = request.POST['searched']
            search_result = client.search(searched, page=page)
            best = search_result.best
            tracks = search_result.tracks
            albums = search_result.albums
            artists = search_result.artists
            playlists = search_result.playlists
            podcasts = search_result.podcasts
            podcast_episodes = search_result.podcast_episodes
            videos = search_result.videos
            best_result = ''
            if best is not None:
                type_ = best.type
                best = best.result
                if type_ in ['track', 'podcast_episode']:
                    best_artists = ''
                    if best.artists:
                        best_artists = ' - ' + ', '.join(artist.name for artist in best.artists)

                    best_result = best.title + best_artists
                elif type_ == 'artist':
                    best_result = best.name
                elif type_ in ['album', 'podcast']:
                    best_artists = ''
                    if best.artists:
                        best_artists = ' - ' + ', '.join(artist.name for artist in best.artists)
                    best_result = best.title + best_artists
                elif type_ == 'playlist':
                    best_result = best.title
                elif type_ == 'video':
                    best_result = best.title + best.text

            if tracks is not None:
                tracks = tracks.results
            if albums is not None:
                albums = albums.results
            if artists is not None:
                artists = artists.results
            if playlists is not None:
                playlists = playlists.results
            if podcasts is not None:
                podcasts = podcasts.results
            if podcast_episodes is not None:
                podcast_episodes = podcast_episodes.results
            if videos is not None:
                videos = videos.results
            

            fav_albums = []
            albums_ = client.users_likes_albums()
            for album in albums_:
                    fav_albums.append(album.album.id)

            fav_artists = []
            artists_ = client.users_likes_artists()
            for artist in artists_:
                fav_artists.append(artist.artist.id) 

            fav_playlists = []
            playlists_ = client.users_likes_playlists()
            for playlist in playlists_:
                fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
            fav_tracks = []
            tracks_ = client.users_likes_tracks().fetch_tracks()
            for track in tracks_:
                    fav_tracks.append(track.id)

            context = {'profile': profile, 'best_result': best_result, 'best': best, 'type': type_, 'tracks': tracks, 'albums': albums, 'artists': artists, 'playlists': playlists,
                    'podcasts': podcasts, 'podcast_episodes': podcast_episodes, 'videos': videos, 'page': page, 'searched': searched, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

            return render(request, "yandex_music_app/yandex_search.html", context)
            









# -----------------------------------------------------TRACK RESULTS-----------------------------------------------------------



@custom_login_required()
def track(request, id):
    if request.method == 'POST':
        track_tag = request.POST.get('tag')
        page = request.POST.get('page')
        sub_track_tag = request.POST.get('sub_tag')
        tagId = request.POST.get('tagId')
        shuffle = request.POST.get('shuffle')
        radio_first_track = request.POST.get('radio_first_track')
        radio_set = request.POST.get('radio_set')
        radio_track_set = request.POST.get('radio_track_set')
        station = request.POST.get('station')
        station_settings2 = request.POST.get('station_settings2')
        station_settings2_initialize = request.POST.get('station_settings2_initialize')
        radio_random_stations = request.POST.get('radio_random_stations')
        radio_personal_stations = request.POST.get('radio_personal_stations')
        station_id_for_from = request.POST.get('station_id_for_from')
        current_stations_origin = request.POST.get('stations_origin')
        track_type = request.POST.get('track_type')
        stored_track = request.POST.get('stored_track')
        track_type_first = request.POST.get('track_type_first')
        track_type_id = request.POST.get('track_type_id')
        foreign_profile = request.POST.get('foreign_profile')
        foreign_profile_next_track = request.POST.get('foreign_profile_next_track')
        playing_track_list_json = request.POST.get('track_list')
        

        profile = Profile.objects.get(user=request.user)
        profile.last_seen = datetime.now()
        profile.save()
        try:
            token = YandexMusic.objects.get(profile=profile).yandex_token
            language = YandexMusic.objects.get(profile=profile).language
        except Exception:
            messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
            return render(request, "yandex_music_app/msg.html")

        else:    
            client = Client(token=token, language=language).init()
        try:
            Track.objects.get(profile=profile)
        except ObjectDoesNotExist:
            Track.objects.create(profile=profile)
        try:    
            RadioHistoryState.objects.get(profile=profile)
        except ObjectDoesNotExist:
            RadioHistoryState.objects.create(profile=profile)
            
        initial_track_list = []
        track_list = []
        last_set = 'false'
        first_set = 'false'
        radio_track_id = None
        track = None
        lyrics = None
        sync_lyrics = None
        _station_id = None
        _station_from = None
        stations_origin = None
        radio_history_json = RadioHistoryState.objects.get(profile=profile)
        existing_track = Track.objects.get(profile=profile)
        if foreign_profile_next_track:
            foreign_profile_existing_track = Track.objects.get(profile=foreign_profile)
        
        if playing_track_list_json:
            playing_track_list = json.loads(playing_track_list_json)
            track_list = playing_track_list
        

        if current_stations_origin:
            stations_origin = current_stations_origin



        if track_tag == 'radio' and not foreign_profile:
            radio = Radio(client) 
            personal_station_track_list_id = f'{track_type}:{track_type_id}'
            random_station_track_list_id = f'{track_type}:{track_type_id}'
                
            if current_stations_origin == 'radio_random_stations' or radio_random_stations:
                _stations = client.rotor_stations_list()
                _station_random_index = floor(len(_stations) * random())
                _station = _stations[_station_random_index].station
                _station_id = f'{_station.id.type}:{_station.id.tag}'
                _station_from = _station.id_for_from

                if radio_first_track:
                    stations_origin = radio_random_stations
                    track_ = radio.start_radio(_station_id, _station_from)
                    radio_track_id = track_.id
                    track_list.append(radio_track_id)
                    if radio_history_json:
                        radio_history_json.radio_history = json.dumps(track_list)
                        radio_history_json.save()
                    else:
                        RadioHistoryState.objects.create(profile = profile, radio_history = json.dumps(track_list))

                elif radio_set:
                    radio_history = None
                    if radio_history_json:
                        radio_history = json.loads(radio_history_json.radio_history)
                    radio_set_tracks = client.rotor_station_tracks(random_station_track_list_id)
                    for track in radio_set_tracks.sequence:
                        if track.track.id not in radio_history:
                            track_list.append(track.track.id)
                            radio_history.append(track.track.id)
                    radio_history_json.radio_history = json.dumps(radio_history)
                    radio_history_json.save()
                    while len(track_list) < 2:
                        reshuffle_radio_set = radio_history[floor(len(radio_history) * random())]
                        reshuffle_radio_set_id = f'{track_type}:{reshuffle_radio_set}'
                        radio_set_tracks = client.rotor_station_tracks(reshuffle_radio_set_id)
                        for track in radio_set_tracks.sequence:
                            if track.track.id not in radio_history:
                                track_list.append(track.track.id)
                                radio_history.append(track.track.id)
                        radio_history_json.radio_history = json.dumps(radio_history)
                        radio_history_json.save()       
                    radio_track_id = track_list[0]
                        
            elif current_stations_origin == 'radio_personal_stations' or radio_personal_stations:
                _station_id = f'{track_type}:{track_type_id}'
                _station_from = station_id_for_from

                if radio_first_track:
                    stations_origin = radio_personal_stations
                    track_ = radio.start_radio(_station_id, _station_from)
                    radio_track_id = track_.id
                    track_list.append(radio_track_id)
                    if radio_history_json:
                        radio_history_json.radio_history = json.dumps(track_list)
                        radio_history_json.save()
                    else:
                        RadioHistoryState.objects.create(profile = profile, radio_history = json.dumps(track_list))

                elif radio_set:
                    radio_history = None
                    if radio_history_json:
                        radio_history = json.loads(radio_history_json.radio_history)
                    radio_set_tracks = client.rotor_station_tracks(personal_station_track_list_id)
                    for track in radio_set_tracks.sequence:
                        if track.track.id not in radio_history:
                            track_list.append(track.track.id)
                            radio_history.append(track.track.id)
                    radio_history_json.radio_history = json.dumps(radio_history)
                    radio_history_json.save()
                    while len(track_list) < 2:
                        reshuffle_radio_set = radio_history[floor(len(radio_history) * random())]
                        reshuffle_radio_set_id = f'{track_type}:{reshuffle_radio_set}'
                        radio_set_tracks = client.rotor_station_tracks(reshuffle_radio_set_id)
                        for track in radio_set_tracks.sequence:
                            if track.track.id not in radio_history:
                                track_list.append(track.track.id)
                                radio_history.append(track.track.id)
                        radio_history_json.radio_history = json.dumps(radio_history)
                        radio_history_json.save()       
                    radio_track_id = track_list[0]

            elif station_settings2 and station_settings2_initialize:
                track_type = station.split(':')[0]
                track_type_id = station.split(':')[1]
                radio_set_tracks = client.rotor_station_tracks(station=station, settings2=station_settings2)
                for track in radio_set_tracks.sequence:
                    track_list.append(track.track.id)
                    if radio_history_json:
                        radio_history_json.radio_history = json.dumps(track_list)
                        radio_history_json.save()
                    else:
                        RadioHistoryState.objects.create(profile = profile, radio_history = json.dumps(track_list))
                id = track_list[0]
                track_type = 'track'
                
            else:
                _station_id = f'{track_type}:{track_type_id}'
                _station_from = station_id_for_from 
                if radio_first_track:
                    track_ = radio.start_radio(_station_id, _station_from)
                    radio_track_id = track_.id
                    track_list.append(radio_track_id)
                    if radio_history_json:
                        radio_history_json.radio_history = json.dumps(track_list)
                        radio_history_json.save()
                    else:
                        RadioHistoryState.objects.create(profile = profile, radio_history = json.dumps(track_list))

                elif radio_set:
                    radio_history = None
                    if radio_history_json:
                        radio_history = json.loads(radio_history_json.radio_history)
                    if station_settings2 is not None:    
                        radio_set_tracks = client.rotor_station_tracks( _station_id, settings2=station_settings2)
                    else:
                        radio_set_tracks = client.rotor_station_tracks( _station_id)

                    for track in radio_set_tracks.sequence:
                        if track.track.id not in radio_history:
                            track_list.append(track.track.id)
                            radio_history.append(track.track.id)
                    radio_history_json.radio_history = json.dumps(radio_history)
                    radio_history_json.save()
                    while len(track_list) < 2:
                        reshuffle_radio_set = radio_history[floor(len(radio_history) * random())]
                        reshuffle_radio_set_id = f'{track_type}:{reshuffle_radio_set}'
                        radio_set_tracks = client.rotor_station_tracks(reshuffle_radio_set_id)
                        for track in radio_set_tracks.sequence:
                            if track.track.id not in radio_history:
                                track_list.append(track.track.id)
                                radio_history.append(track.track.id)
                        radio_history_json.radio_history = json.dumps(radio_history)
                        radio_history_json.save()       
                    radio_track_id = track_list[0]
               
        elif track_tag == 'track' and not foreign_profile:
            if sub_track_tag == 'client':
                tracks_ = client.users_likes_tracks().fetch_tracks()
                for track in tracks_:
                    if 'podcast' not in track.type:
                        initial_track_list.append(track.id)
            elif sub_track_tag == 'charts':
                chart_full = client.chart('world')
                tracks_ = chart_full.chart.tracks
                for track in tracks_:
                    initial_track_list.append(track.track.id)
            elif sub_track_tag == 'artist-tracks':
                artist_track = client.artists_tracks(tagId, page=page)
                tracks_ = artist_track.tracks
                for track in tracks_:
                    initial_track_list.append(track.id)   
            elif sub_track_tag == 'chart-block':
                home = client.landing('chart')
                for block in home.blocks:
                    if block.type == 'chart':
                        block_chart = block.entities
                        for track in block_chart:
                            initial_track_list.append(track.data.track.id)

            
            if len(initial_track_list) > 20:
                if shuffle:
                    track_list.append(initial_track_list[floor(len(initial_track_list) * random())])
                else:    
                    idx = initial_track_list.index(id)
                    new_list = initial_track_list[max(0, idx-5):min(len(initial_track_list), idx+5)]
                    if initial_track_list[-1] == new_list[-1]:
                        new_list.append(initial_track_list[0])
                        track_list = new_list
                        last_set = 'true'
                    elif initial_track_list[0] == new_list[0]:
                        new_list.insert(0, initial_track_list[-1])
                        track_list = new_list
                        first_set = 'true'    
                    else:
                        track_list = new_list
            else:
                if sub_track_tag == 'client':
                    tracks_ = client.users_likes_tracks().fetch_tracks()
                    for track in tracks_:
                        if 'podcast' not in track.type:
                            track_list.append(track.id)
                elif sub_track_tag == 'charts':
                    chart_full = client.chart('world')
                    tracks_ = chart_full.chart.tracks
                    for track in tracks_:
                        track_list.append(track.track.id)
                elif sub_track_tag == 'artist-tracks':
                    artist_track = client.artists_tracks(tagId, page=page)
                    tracks_ = artist_track.tracks
                    for track in tracks_:
                        track_list.append(track.id)   
                elif sub_track_tag == 'chart-block':
                    home = client.landing('chart')
                    for block in home.blocks:
                        if block.type == 'chart':
                            block_chart = block.entities
                            for track in block_chart:
                                track_list.append(track.data.track.id)
                elif sub_track_tag == 'single':
                    single_track = None
                    single_track = client.tracks(id)[0]
                    track_list.append(single_track.id)
        
        
                        

        elif track_tag == 'album' and not foreign_profile:
            tracks_ = []
            album = client.albums_with_tracks(tagId)
            for i, volume in enumerate(album.volumes):
                if len(album.volumes) > 1:
                    tracks_.append(f'💿 Disc {i + 1}')
                tracks_ += volume 
            for track in tracks_:
                if not isinstance(track, str):
                    track_list.append(track.id)
        elif track_tag == 'playlist' and not foreign_profile:
            uid= tagId.split(':')[0]
            kind= tagId.split(':')[1]  
            playlist_tracks = client.users_playlists(user_id=uid, kind=kind).fetch_tracks()
            for track in playlist_tracks:
                    initial_track_list.append(track.track.id)
            if len(initial_track_list) > 20:
                if shuffle:
                    track_list.append(initial_track_list[floor(len(initial_track_list) * random())])
                else:    
                    idx = initial_track_list.index(id)
                    new_list = initial_track_list[max(0, idx-5):min(len(initial_track_list), idx+5)]
                    if initial_track_list[-1] == new_list[-1]:
                        new_list.append(initial_track_list[0])
                        track_list = new_list
                        last_set = 'true'
                    elif initial_track_list[0] == new_list[0]:
                        new_list.insert(0, initial_track_list[-1])
                        track_list = new_list
                        first_set = 'true'    
                    else:
                        track_list = new_list
            else:
                for track in playlist_tracks:
                    track_list.append(track.track.id)
                    
        if track_tag == 'radio' and not foreign_profile:            
            if existing_track:
                if id != '0':
                    radio_track_id = id  
                existing_track.last_track = radio_track_id
                existing_track.tag_id = tagId
                existing_track.tag = track_tag
                existing_track.track_type = track_type
                existing_track.track_type_id = track_type_id
                existing_track.radio_first_track = radio_first_track
                existing_track.radio_set = radio_set
                existing_track.stations_origin = stations_origin
                existing_track.current_stations_origin = current_stations_origin
                existing_track.station_id_for_from = station_id_for_from
                existing_track.station_settings2 = station_settings2
                
               

                existing_track.save()

       
            if radio_first_track or track_type_first:
                track = client.tracks(radio_track_id)[0]
                supplements = client.track_supplement(radio_track_id)
                if supplements.lyrics is None:
                    lyrics = "Lyrics Not Found !"
                else:
                    lyrics = supplements.lyrics.full_lyrics
            else:
                track = client.tracks(id)[0]
                supplements = client.track_supplement(id)
                if supplements.lyrics is None:
                    lyrics = "Lyrics Not Found !"
                else:
                    lyrics = supplements.lyrics.full_lyrics    
                
            try:
                track_lyrics = track.get_lyrics('LRC')
            except Exception:
                sync_lyrics = "Lyrics Not Found !"
            else:
                sync_lyrics = track_lyrics.fetch_lyrics()

            
        else:
            if foreign_profile_next_track:
                id = foreign_profile_existing_track.last_track

            if existing_track:
                existing_track.last_track = id
                existing_track.tag_id = tagId
                existing_track.tag = track_tag
                existing_track.sub_tag = sub_track_tag
                existing_track.track_type = track_type
                existing_track.track_type_id = track_type_id
                existing_track.radio_first_track = radio_first_track
                existing_track.radio_set = radio_set
                existing_track.stations_origin = stations_origin
                existing_track.current_stations_origin = current_stations_origin
                existing_track.station_id_for_from = station_id_for_from
                existing_track.station_settings2 = station_settings2

                existing_track.save()
            
            track = client.tracks(id)[0]
            try:
                track_lyrics = track.get_lyrics('LRC')
            except Exception:
                sync_lyrics = "Lyrics Not Found !"
            else:
                sync_lyrics = track_lyrics.fetch_lyrics()

            supplements = client.track_supplement(id)
            if supplements.lyrics is None:
                lyrics = "Lyrics Not Found !"
            else:
                lyrics = supplements.lyrics.full_lyrics


        download_info = track.get_download_info()
        max_bitrate = max([info.bitrate_in_kbps for info in download_info])
        url = list(filter(lambda t: t.codec == 'mp3' and t.bitrate_in_kbps == max_bitrate, download_info))[0].get_direct_link()
        
    
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track_ in tracks_:
                fav_tracks.append(track_.id)


        context = {'profile': profile, 'foreign_profile': foreign_profile, 'url': url, 'lyrics': lyrics, 'sync_lyrics': sync_lyrics, 'station_settings2': station_settings2, 'track': track, 'radio_set': radio_set, 'track_type': track_type, 'track_type_id': track_type_id, 'track_list': radio_track_set, 'stations_origin': stations_origin, 'radio_first_track': radio_first_track, 'last_set': last_set, 'first_set': first_set, 'tagId': tagId, 'track_tag': track_tag, 'sub_track_tag': sub_track_tag, 'page': page, 'stored_track': stored_track, 'track_list': track_list, 'fav_tracks': fav_tracks}

        return render(request, "yandex_music_app/track.html", context)

    return render(request, "yandex_music_app/track.html", context)






@custom_login_required()
def favourite(request):
    if request.method == 'POST':
        user = request.POST.get('profile_tag')
        if user:
            profile = Profile.objects.get(user=user)
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
                return render(request, "yandex_music_app/msg.html")
            else:    
                client = Client(token=token, language=language).init()
                tracks = []
                tracks_ = client.users_likes_tracks().fetch_tracks()
                for track in tracks_:
                    if 'podcast' not in track.type:
                        tracks.append(track)

        else:      
            try:
                profile = Profile.objects.get(user=request.user)
            except Exception:
                messages.error(request, ("No Registered Account, Login In!"))
                return redirect("profile")
            else:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
                client = Client(token=token, language=language).init()

                tracks = []
                tracks_ = client.users_likes_tracks().fetch_tracks()
                for track in tracks_:
                    if 'podcast' not in track.type:
                        tracks.append(track)
                

        context = {'tracks': tracks}
        return render(request, "yandex_music_app/favourite.html", context)






@custom_login_required()
def album(request, id):
    if request.method == 'POST':
        load_type = request.POST.get('tag')
        profile = Profile.objects.get(user=request.user)
        try:
            token = YandexMusic.objects.get(profile=profile).yandex_token
            language = YandexMusic.objects.get(profile=profile).language
        except Exception:
            messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
            return render(request, "yandex_music_app/msg.html")

        else:    
            client = Client(token=token, language=language).init()
        album = client.albums_with_tracks(id)
        tracks = []
        for i, volume in enumerate(album.volumes):
            if len(album.volumes) > 1:
                tracks.append(f'💿 Disc {i + 1}')
            tracks += volume

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        return render(request, "yandex_music_app/album.html", {'profile': profile, 'id': id, 'load_type': load_type, 'album': album, 'tracks': tracks, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums})

    return render(request, "yandex_music_app/album.html", { 'profile': profile, 'id': id, 'load_type': load_type, 'album': album, 'tracks': tracks, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums})


@custom_login_required()
def artist(request, id, page):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        try:
            token = YandexMusic.objects.get(profile=profile).yandex_token
            language = YandexMusic.objects.get(profile=profile).language
        except Exception:
            messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
            return render(request, "yandex_music_app/msg.html")

        else:    
            client = Client(token=token, language=language).init()
        artist = client.artists(id)[0]
        artist_brief = client.artists_brief_info(id)
        artist_album = client.artists_direct_albums(id, page=page)
        artist_track = client.artists_tracks(id, page=page)
        tracks = artist_track.tracks
        albums = artist_album.albums

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists = client.users_likes_artists()
        for artist in artists:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists = client.users_likes_playlists()
        for playlist in playlists:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        context = {'profile': profile, 'page': page, 'artist': artist, 'artist_album': artist_album, 'id': id,
                   'artist_track': artist_track, 'tracks': tracks, 'albums': albums, 'artist_brief': artist_brief, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}
        return render(request, "yandex_music_app/artist.html", context)

    return render(request, "yandex_music_app/artist.html", context)


@custom_login_required()
def update_artist_tracks(request, id, page):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")

    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        artist = client.artists(id)[0]
        artist_track = client.artists_tracks(id, page=page)
        tracks = artist_track.tracks

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists = client.users_likes_artists()
        for artist in artists:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists = client.users_likes_playlists()
        for playlist in playlists:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        context = {'tracks': tracks, 'artist': artist, 'page': page, 'id': id, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

        return render(request, "yandex_music_app/update_artist_tracks.html", context)


@custom_login_required()
def update_artist_albums(request, id, page):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")

    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        artist = client.artists(id)[0]
        artist_album = client.artists_direct_albums(id, page=page)
        albums = artist_album.albums

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        context = {'albums': albums, 'artist': artist, 'page': page, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

        return render(request, "yandex_music_app/update_artist_albums.html", context)


@custom_login_required()
def playlist(request, uid, kind):
    if request.method == 'POST':
        user = request.POST.get('profile_tag')
        load_type = request.POST.get('tag')
        if user:
            profile = Profile.objects.get(user=user)
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
                return render(request, "yandex_music_app/msg.html")
            else:    
                client = Client(token=token, language=language).init()
                playlist_ = client.users_playlists(user_id=uid, kind=kind)
                playlist_tracks = client.users_playlists(user_id=uid, kind=kind).fetch_tracks()

        else:
            profile = Profile.objects.get(user=request.user)
            try:
                token = YandexMusic.objects.get(profile=profile).yandex_token
                language = YandexMusic.objects.get(profile=profile).language
            except Exception:
                messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
                return render(request, "yandex_music_app/msg.html")
                
                
            else:    
                client = Client(token=token, language=language).init()
            if request.method == 'POST':
                playlist_ = client.users_playlists(user_id=uid, kind=kind)
                playlist_tracks = client.users_playlists(user_id=uid, kind=kind).fetch_tracks()


        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)


        return render(request, "yandex_music_app/playlist.html", {'profile': profile, 'load_type': load_type, 'playlist_tracks': playlist_tracks, 'playlist_': playlist_, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums})

    return render(request, "yandex_music_app/playlist.html", {'profile': profile, 'load_type': load_type, 'playlist_tracks': playlist_tracks, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums})


@custom_login_required()
def podcast(request, id):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        try:
            token = YandexMusic.objects.get(profile=profile).yandex_token
            language = YandexMusic.objects.get(profile=profile).language
        except Exception:
            messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
            return render(request, "yandex_music_app/msg.html")
 
        else:    
            client = Client(token=token, language=language).init()
        podcast = client.albums_with_tracks(id)
        tracks = []
        for i, volume in enumerate(podcast.volumes):
            if len(podcast.volumes) > 1:
                tracks.append(f'💿 Disc {i + 1}')
            tracks += volume


        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)


        return render(request, "yandex_music_app/podcast.html", {'profile': profile, 'tracks': tracks, 'podcast': podcast, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums})

    return render(request, "yandex_music_app/podcast.html", {'profile': profile, 'tracks': tracks, 'podcast': podcast, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums})


@custom_login_required()
def episode(request, id):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        try:
            token = YandexMusic.objects.get(profile=profile).yandex_token
            language = YandexMusic.objects.get(profile=profile).language
        except Exception:
            messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
            return render(request, "yandex_music_app/msg.html")
 
        else:    
            client = Client(token=token, language=language).init()
        track = client.tracks(id)[0]
        download_info = track.get_download_info()
        max_bitrate = max([info.bitrate_in_kbps for info in download_info])
        url = list(filter(lambda t: t.codec == 'mp3' and t.bitrate_in_kbps ==
                   max_bitrate, download_info))[0].get_direct_link()
        

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)


        return render(request, "yandex_music_app/track.html", {'profile': profile, 'url': url, 'track': track, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums})

    return render(request, "yandex_music_app/track.html", {'profile': profile, 'url': url, 'track': track, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums})


@custom_login_required()
def video(request, id):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")
 
    else:
        client = Client(token).init()
    if request.method == 'POST':        
        client = Client(token=token, language=language).init()
        tracks = client.tracks(id)
        for track_ in tracks:
            track = track_
        supplements = client.track_supplement(id)
        videos = supplements.videos
    if not videos or videos is None:
        messages.warning(request, ("Video Not Found !"))
        return render(request, "yandex_music_app/msg.html")
    else:
        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists = client.users_likes_artists()
        for artist in artists:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists = client.users_likes_playlists()
        for playlist in playlists:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)
    
        return render(request, "yandex_music_app/videos.html", {'videos': videos, 'track': track, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums})



@custom_login_required()
def update_best(request, searched, page):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")
    
    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        search_result = client.search(searched, page=page)
        best_result = search_result.best
        best_result = ''
        if best is not None:
            type = best.type
            best = best.result
        if type in ['track', 'podcast_episode']:
            best_artists = ''
            if best.artists:
                best_artists = ' - ' + \
                    ', '.join(artist.name for artist in best.artists)
            best_result = best.title + best_artists
        elif type == 'artist':
            best_result = best.name
        elif type in ['album', 'podcast']:
            best_result = best.title
        elif type == 'playlist':
            best_result = best.title
        elif type == 'video':
            best_result = f'{best.title} {best.text}'

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)    

        context = {'best_result': best_result, 'type': type,
                   'page': page, 'searched': searched, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

        return render(request, "yandex_music_app/update_best.html", context)


@custom_login_required()
def update_tracks(request, searched, page):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")

    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        search_result = client.search(searched, page=page)
        tracks = search_result.tracks
        if tracks is not None:
            tracks = tracks.results

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        context = {'tracks': tracks, 'page': page, 'searched': searched, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

        return render(request, "yandex_music_app/update_tracks.html", context)


@custom_login_required()
def update_albums(request, searched, page):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")
 
    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        search_result = client.search(searched, page=page)
        albums = search_result.albums
        if albums is not None:
            albums = albums.results

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        context = {'albums': albums, 'page': page, 'searched': searched, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

        return render(request, "yandex_music_app/update_albums.html", context)


@custom_login_required()
def update_artists(request, searched, page):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")

    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        search_result = client.search(searched, page=page)
        artists = search_result.artists
        if artists is not None:
            artists = artists.results


        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        context = {'artists': artists, 'page': page, 'searched': searched, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

        return render(request, "yandex_music_app/update_artists.html", context)


@custom_login_required()
def update_playlists(request, searched, page):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")

    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        search_result = client.search(searched, page=page)
        playlists = search_result.playlists
        if playlists is not None:
            playlists = playlists.results

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        context = {'playlists': playlists, 'page': page, 'searched': searched, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

        return render(request, "yandex_music_app/update_playlists.html", context)


@custom_login_required()
def update_podcasts(request, searched, page):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")
   
    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        search_result = client.search(searched, page=page)
        podcasts = search_result.podcasts
        if podcasts is not None:
            podcasts = podcasts.results

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        context = {'podcasts': podcasts, 'page': page, 'searched': searched, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

        return render(request, "yandex_music_app/update_podcasts.html", context)


@custom_login_required()
def update_podcast_episodes(request, searched, page):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")

    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        search_result = client.search(searched, page=page)
        podcast_episodes = search_result.podcast_episodes
        if podcast_episodes is not None:
            podcast_episodes = podcast_episodes.results

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        context = {'podcast_episodes': podcast_episodes,
                   'page': page, 'searched': searched, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

        return render(request, "yandex_music_app/update_episodes.html", context)


@custom_login_required()
def update_videos(request, searched, page):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")

    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        search_result = client.search(searched, page=page)
        videos = search_result.videos
        if videos is not None:
            videos = videos.results

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
                fav_albums.append(album.album.id)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id) 

        fav_playlists = []
        playlists_ = client.users_likes_playlists()
        for playlist in playlists_:
            fav_playlists.append(f'{playlist.playlist.kind}{playlist.playlist.uid}')
        fav_tracks = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
                fav_tracks.append(track.id)

        context = {'videos': videos, 'page': page, 'searched': searched, 'fav_artists': fav_artists, 'fav_playlists': fav_playlists, 'fav_tracks': fav_tracks, 'fav_albums': fav_albums}

        return render(request, "yandex_music_app/update_videos.html", context)


@custom_login_required()
def suggestion_yandex_music_search_result(request):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")

    else:    
        client = Client(token=token, language=language).init()

    if request.method == 'POST':
        searched = request.POST['searched']
        suggestions = client.search_suggest(searched).suggestions
        return render(request, "yandex_music_app/suggestion.html", {'suggestions': suggestions})



@custom_login_required()
def lyrics(request, id):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")

    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        tracks = client.tracks(id)
        for track_ in tracks:
            track = track_
        supplements = client.track_supplement(id)
        if supplements.lyrics is None:
            messages.warning(request, ("Lyrics Not Found !"))
            return render(request, "yandex_music_app/msg.html")
        else:
            lyrics = supplements.lyrics.full_lyrics
            return render(request, "yandex_music_app/lyrics.html", {'lyrics': lyrics, 'track': track})



@custom_login_required()
def toggle_like(request):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        error = Exception
        return render(request, "yandex_music_app/like.html", {'error': error})
    else:    
        client = Client(token=token, language=language).init()
        if request.method == 'POST':
            tag = request.POST.get('tag')
            id = request.POST.get('id')
            location = request.POST.get('location')
            success = None
            if tag == 'track_like':
                success = client.users_likes_tracks_add(id)
            elif tag == 'track_dislike':
                success = client.users_likes_tracks_remove(id)
            elif tag == 'album_like':
                success = client.users_likes_albums_add(id)
            elif tag == 'album_dislike':
                success = client.users_likes_albums_remove(id)    
            elif tag == 'artist_like':
                success = client.users_likes_artists_add(id)
            elif tag == 'artist_dislike':
                success = client.users_likes_artists_remove(id)        
            elif tag == 'playlist_like':
                success = client.users_likes_playlists_add(id)
            elif tag == 'playlist_dislike':
                success = client.users_likes_playlists_remove(id)    
             
            return render(request, "yandex_music_app/toggle_like.html", {'success': success, 'tag': tag, 'id': id, 'location': location})







@custom_login_required()
def toggle_visibility(request):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        error = Exception
        return render(request, "yandex_music_app/like.html", {'error': error})
    else:    
        client = Client(token=token, language=language).init()
        if request.method == 'POST':
            tag = request.POST.get('tag')
            id = request.POST.get('id')
            playlist = None
            if tag == 'private':
                playlist = client.users_playlists_visibility(id, tag)
            elif tag == 'public':
                playlist = client.users_playlists_visibility(id, tag)
    
            return render(request, "yandex_music_app/toggle_visibility.html", {'playlist': playlist, 'id': id})



@custom_login_required()
def to_album(request, id):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
        return render(request, "yandex_music_app/msg.html")
    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        load_type = request.POST.get('tag')
        track_ = client.tracks(id)
        for track in track_:
            for album_ in track.albums:
                album = client.albums_with_tracks(album_.id)
                tracks = []
                for i, volume in enumerate(album.volumes):
                    if len(album.volumes) > 1:
                        tracks.append(f'💿 Disc {i + 1}')
                    tracks += volume

        fav_albums = []
        albums_ = client.users_likes_albums()
        for album in albums_:
            if  album.album.type != 'podcast':
                fav_albums.append(album.album.id)

        return render(request, "yandex_music_app/album_type.html", {'album': album, 'load_type': load_type, 'album_': album_, 'tracks': tracks, 'id': id, 'fav_albums': fav_albums})




@custom_login_required()
def to_artist(request, id):
    profile = Profile.objects.get(user=request.user)
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In To Get Full Access!"))
        return render(request, "yandex_music_app/msg.html")
    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        tag = request.POST.get('tag')
        artists = []
        if tag == 'track':
            track_ = client.tracks(id)
            for track in track_:
                for artist in track.artists:
                    artists.append(artist)
        elif tag == 'album':
            album_ = client.albums(id)
            for album in album_:
                for artist in album.artists:
                    artists.append(artist)

        fav_artists = []
        artists_ = client.users_likes_artists()
        for artist in artists_:
            fav_artists.append(artist.artist.id)
    
        return render(request, "yandex_music_app/artists_intro.html", {'artists': artists, 'id': id, 'fav_artists': fav_artists})



@custom_login_required()
def add_tracks(request, id):
    profile = Profile.objects.get(user=request.user)
    delete = request.POST.get('delete')
    add_track = True
    try:
        token = YandexMusic.objects.get(profile=profile).yandex_token
        language = YandexMusic.objects.get(profile=profile).language
    except Exception:
        messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
        return render(request, "yandex_music_app/msg.html")

    else:    
        client = Client(token=token, language=language).init()
    if request.method == 'POST':
        track = client.tracks(id)[0]
        avatar_url = track.cover_uri
        title = track.title
        explicit = track.content_warning
        artists = ', '.join(artist.name for artist in track.artists)
        existing_track = YandexMusicTrack.objects.filter(track_id=id)
        profile_tracks = YandexMusicTrack.objects.filter(profile=profile)
        if existing_track and delete:
            existing_track.delete()
            return render(request, "yandex_music_app/msg.html", {'profile': profile, 'add_track': add_track, 'delete': delete})
        
        if profile_tracks.count() < 3:

            if existing_track:
                existing_track.delete()
                YandexMusicTrack.objects.create(profile=profile, track_id=id, track_name=title, track_artists= artists,  avatar_url=avatar_url, explicit_state=explicit)
            else:
                YandexMusicTrack.objects.create(profile=profile, track_id=id, track_name=title, track_artists=artists,  avatar_url=avatar_url, explicit_state=explicit)
            messages.success(request, ("Done ✔"))
            return render(request, "yandex_music_app/msg.html", {'profile': profile, 'add_track': add_track})
        else:
            messages.warning(request, ("Exceeded 3 tracks!"))
            return render(request, "yandex_music_app/msg.html", {'profile': profile, 'add_track': add_track})           


# ---------------------------------------------------------------------------------------------------------------------------



@custom_login_required()
def collections(request):
    if request.method == 'POST':         
        user = request.POST.get('profile_tag')
        profile = Profile.objects.get(pk=user)
        language = None
        token = None

        try:
            token = YandexMusic.objects.get(profile=profile).yandex_token
            language = YandexMusic.objects.get(profile=profile).language
        except Exception:
            messages.error(request, ("No Registered Yandex Account, Login In And Try Again!"))
            return render(request, "yandex_music_app/msg.html")
        
        else:    
            client = Client(token=token, language=language).init()
            
        tracks = []
        albums = []
        episode_tracks = []
        podcast_albums = []
        tracks_ = client.users_likes_tracks().fetch_tracks()
        for track in tracks_:
            if 'podcast' not in track.type:
                tracks.append(track)
            else:
                episode_tracks.append(track)    
        playlists = client.users_likes_playlists()
        user_playlists = client.users_playlists_list()

        
        albums_ = client.users_likes_albums()
        for album in albums_:
            if  album.album.type != 'podcast':
                albums.append(album.album)
            else:
                podcast_albums.append(album.album)    

        artists = client.users_likes_artists()

        return render(request, "yandex_music_app/collections_public.html", {'user': user, 'tracks': tracks, 'playlists': playlists, 'user_playlists': user_playlists, 'albums': albums, 'artists': artists, 'episode_tracks': episode_tracks, 'podcast_albums': podcast_albums})