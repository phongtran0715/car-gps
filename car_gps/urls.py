from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from authentication.views import (
        home_screen_view,
        registration_view,
        login_view,
        logout_view,
        activate_view
    )
from user_profile.views import upload_image_view
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url


urlpatterns = [
    
    #APi route
    re_path('api/(?P<version>(v1|v2))/', include('authentication.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('tracking_info.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('user_profile.urls')),

    path('activate/<uidb64>/<token>/',
        activate_view, name='activate'),

    url(r'^api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # Web route
    path('admin/', admin.site.urls),
    path('', home_screen_view, name="home"),
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('upload/', upload_image_view, name="uploaed-image"),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    # path('password_change/done/',
    #      auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
    #      name='password_change_done'),

    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
    #      name='password_change'),

    # path('password_reset/done/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
    #      name='password_reset_done'),

    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
    #      name='password_reset'),

    # path('reset/done/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    #      name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
