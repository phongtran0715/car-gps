from django.urls import path, include

from .views import ChangePasswordView, LogoutView, UserRegistrationAPIView, UserLoginAPIView

urlpatterns = [
    path('auth/login/', UserLoginAPIView.as_view(), name="auth-login"),
    path('auth/register/', UserRegistrationAPIView.as_view(), name="auth-register"),
    path('auth/reset-password/', ChangePasswordView.as_view(), name="auth-reset-password"),
    path('auth/logout/', LogoutView.as_view(), name="auth-logout"),
    path('auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
