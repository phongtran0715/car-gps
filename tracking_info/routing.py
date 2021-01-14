from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/tracking/(?P<user_name>\w+)/$', consumers.TrackingConsumer.as_asgi()),
]