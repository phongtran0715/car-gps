from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import ChangePasswordView, UserRegistrationAPIView, UserLoginAPIView, HelloView, LogoutView

urlpatterns = [
    path('hello/', HelloView.as_view(), name="hello"),
    path('auth/login/', UserLoginAPIView.as_view(), name="auth-login"),
    path('auth/register/', UserRegistrationAPIView.as_view(), name="auth-register"),
    path('auth/change_password/', ChangePasswordView.as_view(), name="auth-reset-password"),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
