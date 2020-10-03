from django.urls import path

from user_profile.views import GetUserProfile, UpdateUserProfile, ChangeAvatar

urlpatterns = [
    path('profile/', GetUserProfile.as_view(), name='get-profile'),
    path('profile/update/', UpdateUserProfile.as_view(), name='update-profile'),
    path('profile/avatar/update/', ChangeAvatar.as_view(), name='change-avatar'),
]
