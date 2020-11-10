from rest_framework import serializers
from .models import VinatrackSettings

class VinatrackSettingsSerializer(serializers.ModelSerializer):
	class Meta:
		model = VinatrackSettings
		fields = ('notification', 'language', 'map_display', 'distance_unit', 'refresh_interval', 'theme')