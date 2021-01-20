from django.urls import path, re_path
from .views import (
	get_notification_view
	)


urlpatterns = [
	path('notifications', get_notification_view, name='get-notifications'),
]