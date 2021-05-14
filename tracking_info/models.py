from django.db import models

# Create your models here.
from rest_framework_simplejwt.state import User


class CarTrackingInfo(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_info')
	longitude = models.DecimalField(max_digits=20, decimal_places=17, null=True)
	latitude = models.DecimalField(max_digits=20, decimal_places=17, null=True)
	gas = models.FloatField(blank=False, default=0)
	gps_status = models.BooleanField(blank=False, default=False)
	speed = models.FloatField(blank=False, default=0)
	odometer = models.FloatField(blank=False, default=0)
	is_stop = models.BooleanField(blank=False, default=False)
	timestamp = models.DateTimeField(blank=True, null=True)

	class Meta:
		db_table = "car_tracking"
		ordering = ['timestamp']
		indexes = [
			models.Index(fields=['timestamp', 'user_id']),
		]

	def __str__(self):
		return '{}'.format(self.user_id)
