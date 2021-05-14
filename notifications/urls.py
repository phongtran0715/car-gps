from django.urls import path
from .views import api_get_notification_view

urlpatterns = [
    path('notifications/', api_get_notification_view),
]
