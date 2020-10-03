from django.contrib.auth.models import User
from rest_framework import generics, permissions, authentication

# Create your views here.
from rest_framework.permissions import IsAuthenticated

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class GetUserProfile(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)


class UpdateUserProfile(generics.UpdateAPIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    queryset = UserProfile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer
    lookup_field = 'id'

    def get_object(self):
        return User.objects.get(id=self.request.user.id)


class ChangeAvatar(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
