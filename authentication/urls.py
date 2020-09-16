from django.urls import path, include

from .views import ChangePasswordView, UserRegistrationAPIView, UserLoginAPIView, HelloView, \
    LogoutAndBlacklistRefreshTokenForUserView, sendmail

urlpatterns = [
    path('hello/', HelloView.as_view(), name="hello"),
    path('sendmail', sendmail, name='sendmail'),
    path('auth/login/', UserLoginAPIView.as_view(), name="auth-login"),
    path('auth/register/', UserRegistrationAPIView.as_view(), name="auth-register"),
    path('auth/change_password/', ChangePasswordView.as_view(), name="auth-reset-password"),
    path('auth/logout/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name="auth-logout"),
    path('auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
