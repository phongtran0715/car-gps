from django.urls import path

from user_profile.views import (
    update_profile_view,
    profile_view,
    change_avatar_view)

urlpatterns = [
    path('profile/', profile_view, name='get-profile'),
    path('profile/update/', update_profile_view, name='update-profile'),
    path('profile/avatar/update/', change_avatar_view, name='change-avatar'),
]
