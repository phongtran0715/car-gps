from django.db import models

# Create your models here.
from rest_framework_simplejwt.state import User


class CarTrackingInfo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_info')
    longitude = models.DecimalField(max_digits=20, decimal_places=17, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=17, null=True)
    gas = models.FloatField(blank=True, null=True)
    gps_status = models.BooleanField(blank=True, default=False)
    speed = models.FloatField(blank=True, null=True)
    odometer = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "car_tracking"
        ordering = ['-id']
