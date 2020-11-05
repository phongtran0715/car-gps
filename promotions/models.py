from django.db import models

# Create your models here.

class Promotions(models.Model):
	title = models.CharField(max_length=250)
	image = models.ImageField(max_length=1024)
	url = models.CharField(max_length=1024, blank=True)
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "promotions"
		ordering = ['updated_at']