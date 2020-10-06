from django.urls import path

from tracking_info.views import (
    get_live_tracking_view,
    get_history_tracking_view,
    insert_tracking_info_view
)

urlpatterns = [
    path('car/live/', get_live_tracking_view, name='get-live-tracking'),
    path('car/report/', get_history_tracking_view, name='get-history-tracking'),
    path('car/live/update/', insert_tracking_info_view, name='insert-tracking'),
]
