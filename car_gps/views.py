from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authentication.forms import AccountAuthenticationForm, RegistrationForm
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view, permission_classes
import requests, json
from user_profile.models import UserProfile
from django.template import loader
from django.http import HttpResponse


def home_screen_view(request):
	return render(request, "car_gps/index.html")

def news_view(request):
	return render(request, "car_gps/blog.html")

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

			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'car_gps/register.html', context)


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
	print(context)

	return render(request, "car_gps/login.html", context)


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
			return render(request, "registration/password_reset_complete.html")
		else:
			return render(request, "registration/api_password_change.html", context)
	else:
		return render(request, "registration/api_password_change.html", context)

def vinatrack_html_view(request):
	context = {}
	# The template to be loaded as per gentelella.
	# All resource paths for gentelella end in .html.

	# Pick out the html file name from the url. And load that template.
	load_template = request.path.split('/')[-1]
	template = loader.get_template('car_gps/' + load_template)
	return HttpResponse(template.render(context, request))
