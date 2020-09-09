from django.urls import path, include

from .serializers import UserSerializer
from .views import LoginView, RegisterUsers, ChangePasswordView, LogoutView

urlpatterns = [
    path('auth/login/', LoginView.as_view(serializer_class=UserSerializer), name="auth-login"),
    path('auth/register/', RegisterUsers.as_view(serializer_class=UserSerializer), name="auth-register"),
    path('auth/reset-password/', ChangePasswordView.as_view(serializer_class=UserSerializer), name="auth-reset-password"),
    path('auth/logout/', LogoutView.as_view(serializer_class=UserSerializer), name="auth-logout"),
    path('auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
