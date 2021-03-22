from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authentication.forms import AccountAuthenticationForm, RegistrationForm
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view, permission_classes
import requests, json


def home_screen_view(request):
    context = {}
    accounts = User.objects.all()
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    context['accounts'] = accounts
    context['home_image'] = protocol + '://' + request.get_host() + "/media/home2.jpg"

    return render(request, "home/home.html", context)


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # create user profile
            UserProfile.objects.create(id=user.id)
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'home/register.html', context)


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username= username, password=password)

            if user:
                login(request, user)
                return redirect("home")
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "home/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')


def reset_password_view(request, token):
    context = {}
    if request.method == 'POST':
        # TODO : check matching password
        data = {}
        data['password'] = request.POST['password']
        data['token'] = token
        print(request.build_absolute_uri('confirm/'))
        resp = requests.post(request.build_absolute_uri('confirm/'), data=data)
        if resp.status_code == 200:
            return redirect('password_reset_complete')
        else:
            return render(request, "registration/api_password_change.html", context)
    else:
        return render(request, "registration/api_password_change.html", context)
