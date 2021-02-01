from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Notifications(models.Model):
	title = models.CharField(max_length=128)
	body = models.CharField(max_length=250)
	image = models.ImageField(blank=True, default="null")
	url = models.CharField(max_length=1024, blank=True)
	user_id = models.ManyToManyField(User, blank=True)
	created_at = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = "notifications"
		ordering = ['created_at']