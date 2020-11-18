from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.state import User


# Create your models here.
class VinatrackSettings(models.Model):
	NOTIFICATION =(
		(0, False),
		(1, True)
	)

	LANGUAGE = (
		(0, "vi"),
		(1, "en"),
		(2, "cn")
	)

	MAP_DISPLAY = (
		(0, "map"),
		(1, "satellite")
	)

	DISTANCE_UNIT = (
		(0, "km"),
		(1, "miles")
	)

	DATETIME_FORMAT = (
		(0, "YYYY-MM-DD HH:mm:ss"),
		(1, "YYYY-DD-MM HH:mm:ss"),
		(2, "YYYY-DD-MM HH:mm"),
		(3, "YYYY/MM/DD HH:mm:ss"),
		(4, "YYYY/DD/MM HH:mm:ss"),
		(5, "YYYY/DD/MM HH:mm")
	)

	REFRESH_INTERVAL = (
		(0, 10),
		(2, 20),
		(3, 30)
	)

	THEME = (
		(0, 'dark'),
		(1, 'light')
	)

	id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='settings')
	notification = models.BooleanField(default=True, choices=NOTIFICATION)
	language = models.CharField(default="vi", choices=LANGUAGE, max_length=3)
	map_display = models.CharField(default="map", choices=MAP_DISPLAY, max_length=128)
	datetime_format = models.CharField(default="YYYY-MM-DD HH:mm:ss", choices=DATETIME_FORMAT, max_length=256)
	distance_unit = models.CharField(default="km", choices=DISTANCE_UNIT, max_length=16)
	refresh_interval = models.IntegerField(default=20, choices=REFRESH_INTERVAL)
	theme = models.CharField(default='light', choices=THEME, max_length=64)

	class Meta:
		db_table = "settings"
		ordering = ('id',)

	# @receiver(post_save, sender=User)
	# def create_or_update_settings(sender, instance, created, **kwargs):
	# 	if created:
	# 		VinatrackSettings.objects.create(id=instance)
	# 	instance.settings.save()
