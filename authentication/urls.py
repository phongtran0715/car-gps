from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import ChangePasswordView, UserRegistrationAPIView, UserLoginAPIView, LogoutView
from django.conf.urls import include, url

urlpatterns = [
    path('auth/login/', UserLoginAPIView.as_view(), name="auth-login"),
    path('auth/register/', UserRegistrationAPIView.as_view(), name="auth-register"),
    
    path('auth/change_password/', ChangePasswordView.as_view(), name="auth-reset-password"),

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
