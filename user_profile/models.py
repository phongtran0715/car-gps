from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.state import User
import time, os
from uuid import uuid4


class UserProfile(models.Model):
	id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
	car_name = models.CharField(max_length=100)
	plate_number = models.CharField(max_length=50, default='NA')
	avatar = models.ImageField(max_length=1024, blank=True)

	class Meta:
		db_table = "user_profile"
		ordering = ('id',)
		indexes = [
			models.Index(fields=['id']),
		]

	def __str__(self):
		if self.car_name != "":
			return '{}-{}'.format(self.id, self.car_name)
		else:
			return '{}'.format(self.id)

	@receiver(post_save, sender=User)
	def create_or_update_user_profile(sender, instance, created, **kwargs):
		if created:
			UserProfile.objects.create(id=instance)
			instance.profile.avatar = '/avatar/default/default.png'
		instance.profile.save()
