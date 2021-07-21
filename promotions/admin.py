from django.contrib import admin
from .models import Promotions


class PromotionsAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Promotions._meta.fields if field.name != "id"]
	list_filter = ['title', 'active']


admin.site.register(Promotions, PromotionsAdmin)
