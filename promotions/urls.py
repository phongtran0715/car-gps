from django.urls import path
from .views import api_get_promotion_view

urlpatterns = [
    path('promotions/', api_get_promotion_view),
]
