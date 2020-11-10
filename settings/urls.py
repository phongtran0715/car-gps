from django.urls import path
from .views import (
	settings_view,
	update_settings_view,
	reset_default_view
)

urlpatterns = [
    path('setting/', settings_view, name='get-setting'),
    path('setting/update/', update_settings_view, name='update-setting'),
    path('setting/reset/', reset_default_view, name='reset-setting'),
]