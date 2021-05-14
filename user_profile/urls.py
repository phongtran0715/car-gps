from django.urls import path
from .views import (
    update_profile_view,
    profile_view,
    change_avatar_view)

urlpatterns = [
    path('profile/', profile_view),
    path('profile/update/', update_profile_view),
    path('profile/avatar/update/', change_avatar_view),
]
