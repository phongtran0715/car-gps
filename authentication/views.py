from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegistrationSerializer, ChangePasswordSerializer, UserLoginSerializer, \
    RefreshTokenSerializer


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
            data = {
                "message": "The user was created successfully"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            "message": "Validation errors in your request",
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
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_201_CREATED)
        data = {
            "message": "Validation errors in your request",
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
            "message": "Validation errors in your request",
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
            "message": "Validation errors in your request",
            "errors": serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
