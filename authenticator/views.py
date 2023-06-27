from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from yandex_music_app.models import Profile, State, Media
from django.core.exceptions import ObjectDoesNotExist
from .forms import RegisterUserForm


# Create your views here.

# login user

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.error(
                request, ("Account Does Not Exist, Try Again!"))
            return redirect('login_user')
        profile = Profile.objects.filter(user__username=user)
        if profile:
            login(request, user)
            profile = Profile.objects.get(user=request.user)
            messages.success(
                request, ("Logged In"))
            return redirect('home')
        else:
            messages.error(
                request, ("There Was An Error Logging In, Try Again!"))
            return redirect('login_user')
        
    else:

        return render(request, 'authenticator/login.html')


# logout user

def logout_user(request):
    profile = Profile.objects.get(user=request.user)
    profile.is_online = False
    profile.save()
    logout(request)
    messages.success(request, ("You Were Logged Out"))
    return redirect('login_user')


# register user


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            profile = Profile.objects.create(user=user)
            profile.save()
            login(request, user)
            profile = Profile.objects.get(user=request.user)
            State.objects.create(profile_id=profile.id)
            Media.objects.create(profile=profile, name='twitter', suffix='')
            Media.objects.create(profile=profile, name='vk', suffix='')
            Media.objects.create(profile=profile, name='facebook', suffix='')
            Media.objects.create(profile=profile, name='instagram', suffix='')
            messages.success(request, ("Registration Successful"))
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'authenticator/sign_up.html', {
        'form': form,
    })