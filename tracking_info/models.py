from django.db import models

# Create your models here.
from rest_framework_simplejwt.state import User


class CarTrackingInfo(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_info')
	longitude = models.DecimalField(max_digits=20, decimal_places=7, null=True)
	latitude = models.DecimalField(max_digits=20, decimal_places=7, null=True)
	gas = models.DecimalField(blank=False, default=0, max_digits=10, decimal_places=2)
	gps_status = models.BooleanField(blank=False, default=False)
	speed = models.DecimalField(blank=False, default=0, max_digits=10, decimal_places=5)
	distance = models.DecimalField(blank=False, default=0, max_digits=10, decimal_places=5)
	odometer = models.DecimalField(blank=False, default=0, max_digits=10, decimal_places=2)
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
