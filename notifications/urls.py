from django.urls import path, re_path
from . import views

urlpatterns = [
	path('notifications', views.get_notification_view, name='get-notifications'),
	path('notifications/new/', views.notification_new, name='notification_new'),
]