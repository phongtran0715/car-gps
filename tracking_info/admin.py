from django.contrib import admin
from tracking_info.models import CarTrackingInfo


@admin.register(CarTrackingInfo)
class CarTrakingInfoAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CarTrackingInfo._meta.fields]
    list_filter = ("user_id", "is_stop",)