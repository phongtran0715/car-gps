from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.forms import (
        AccountAuthenticationForm,
        RegistrationForm)
from .serializers import (
        UserRegistrationSerializer,ChangePasswordSerializer,
        UserLoginSerializer, RefreshTokenSerializer)
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from user_profile.models import UserProfile
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils.translation import gettext as _


class UserRegistrationAPIView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            user = authenticate(username=request.data['username'], password=request.data['password'])
            user.save()

            # send confirmation email
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('authentication/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':account_activation_token.make_token(user),
            })
            print('message : {}'.format(message))
            to_email = request.data['email']
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            data = {
                "message": _("The user was created successfully")
            }
            return Response(data, status=status.HTTP_201_CREATED)
            
        data = {
            "message": _("Validation errors in your request"),
            "errors": serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                data = {
                    "id": user.id,
                    "username": user.username,
                    "is_active": user.profile.is_active,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_201_CREATED)
        data = {
            "message": _("Validation errors in your request"),
            "errors": serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check current password
            if not self.object.check_password(serializer.data.get("current_password")):
                return Response({"current_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            # revoke current refresh token
            try:
                RefreshToken(serializer.data.get("refresh")).blacklist()
            except TokenError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            data = {
                "message": "Password updated successfully"
            }

            return Response(data, status=status.HTTP_200_OK)
        data = {
            "message": _("Validation errors in your request"),
            "errors": serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Success"
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            "message": _("Validation errors in your request"),
            "errors": serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


def activate_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.profile.is_active = True
        user.save()
        login(request, user)
        return HttpResponse(_('Thank you for your email confirmation. Now you can login your account.'))
    else:
        return HttpResponse(_('Activation link is invalid!'))


# web UI
def home_screen_view(request):
    context = {}
    accounts = User.objects.all()
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    context['accounts'] = accounts
    context['home_image'] = protocol + '://' + request.get_host() + "/media/home2.jpg"

    return render(request, "home.html", context)


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
    return render(request, 'register.html', context)


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

    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')
