from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from authentication.views import activate_view
from promotions.views import api_get_promotion_view
from notifications.views import api_get_notification_view
from django.contrib.auth import views as auth_views
from tracking_info.views import index, room
from . import views

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'devices', FCMDeviceAuthorizedViewSet)


admin.site.site_header = 'Vinatrack Admin'
admin.site.site_title = 'Vinatrack Admin'
admin.site.index_title = u'Vinatrack'

urlpatterns = [
	
	#API route
	re_path('api/(?P<version>(v1|v2))/', include('authentication.urls')),
	re_path('api/(?P<version>(v1|v2))/', include('tracking_info.urls')),
	re_path('api/(?P<version>(v1|v2))/', include('user_profile.urls')),
	re_path('api/(?P<version>(v1|v2))/', include('promotions.urls')),
	re_path('api/(?P<version>(v1|v2))/', include('notifications.urls')),
	
	path('api/password_reset/<token>', views.reset_password_view, name='api_password_reset_verify_token'),
	url(r'^api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
	re_path(r'^api/(?P<version>(v1|v2))/', include(router.urls)),

	# Web route
	path('admin/', admin.site.urls),
	path('', views.home_screen_view, name="index"),
	path('tin-tuc/', views.news_view, name="news"),
	re_path(r'^.*\.html', views.vinatrack_html_view, name='vinatrack_news'),

	path('activate/<uidb64>/<token>/',activate_view, name='activate'),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
