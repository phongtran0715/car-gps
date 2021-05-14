from django.urls import path

from .views import (
    get_live_tracking_view,
    get_history_tracking_view,
    insert_tracking_info_view,
    get_history_stop_view
)

urlpatterns = [
    path('car/live/', get_live_tracking_view),
    path('car/report/', get_history_tracking_view),
    path('car/report/stop/', get_history_stop_view),
    path('car/live/update/', insert_tracking_info_view),
]
