from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.state import User


class UserProfile(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    car_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    imei = models.CharField(max_length=50, null=True)
    plat_number = models.CharField(max_length=50, null=True)
    avatar = models.CharField(max_length=1024, blank=True)

    class Meta:
        db_table = "user_profile"
        ordering = ('id',)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(id=instance)
        instance.profile.save()
