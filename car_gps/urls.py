from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from authentication.views import activate_view
from home.views import reset_password_view
from promotions.views import api_get_promotion_view
from notifications.views import api_get_notification_view
from django.contrib.auth import views as auth_views
from tracking_info.views import index, room

urlpatterns = [
    
    #API route
    re_path('api/(?P<version>(v1|v2))/', include('authentication.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('tracking_info.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('user_profile.urls')),
    
    path('api/password_reset/<token>', reset_password_view, name='api_password_reset_verify_token'),
    url(r'^api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
    re_path(r'^api/(?P<version>(v1|v2))/promotions/', api_get_promotion_view),
    re_path(r'^api/(?P<version>(v1|v2))/notifications/', api_get_notification_view),

    # Web route
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('promotions.urls')),
    path('', include('notifications.urls')),
    path('car/tracking/', index, name='tracking_index'),
    path('car/tracking/<str:room_name>/', room, name='room'),

    path('activate/<uidb64>/<token>/',activate_view, name='activate'),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
