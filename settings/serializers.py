from rest_framework import serializers
from .models import VinatrackSettings

class VinatrackSettingsSerializer(serializers.ModelSerializer):
	notification = serializers.BooleanField(source='get_notification_display')
	language = serializers.CharField(source='get_language_display')
	map_display = serializers.CharField(source='get_map_display_display')
	datetime_format = serializers.CharField(source='get_datetime_format_display')
	distance_unit = serializers.CharField(source='get_distance_unit_display')
	refresh_interval = serializers.IntegerField(source='get_refresh_interval_display')
	theme = serializers.CharField(source='get_theme_display')
	
	class Meta:
		model = VinatrackSettings
		fields = ('notification', 'language', 'map_display', 'datetime_format', 'distance_unit', 'refresh_interval', 'theme')