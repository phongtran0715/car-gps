from django.urls import path, re_path
from .views import (
	get_promotion_view, 
	create_promotion_view,
	update_promotion_view,
	delete_promotion_view,
	api_get_promotion_view
)


urlpatterns = [
	path('promotions', get_promotion_view, name='get-promotions'),
	path('promotions/new/', create_promotion_view, name='create-promotions'),
	path('promotions/<int:pk>/update/', update_promotion_view, name='update-promotions'),
	path('promotions/<int:pk>/delete/', delete_promotion_view, name='delete-promotions'),
]