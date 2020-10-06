from rest_framework import serializers

from tracking_info.models import CarTrackingInfo


class CarTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarTrackingInfo
        fields = ('latitude', 'longitude', 'gas', 'gps_status', 'speed', 'odometer', 'timestamp')
