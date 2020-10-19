from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.state import User
import time, os
from uuid import uuid4


class UserProfile(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    car_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    imei = models.CharField(max_length=50, null=True)
    plate_number = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=False)
    avatar = models.ImageField(max_length=1024, blank=True)

    class Meta:
        db_table = "user_profile"
        ordering = ('id',)

    def __str__(self):
        return self.car_name

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(id=instance)
        instance.profile.avatar = '/avatar/default/default.png'
        instance.profile.save()
