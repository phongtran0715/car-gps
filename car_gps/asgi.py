"""
ASGI config for car_gps project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import tracking_info.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_gps.settings')

application = ProtocolTypeRouter({
	"http": get_asgi_application(),
	# Just HTTP for now. (We can add other protocols later.)
	"websocket": AuthMiddlewareStack(
		URLRouter(
			tracking_info.routing.websocket_urlpatterns
		)
	),
})
