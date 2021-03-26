from django.contrib import admin
from .models import Notifications


# Register your models here.
# admin.site.register(Notifications)

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
	list_display = ('title', 'body', 'created_at')
	list_filter = ('title', 'created_at' )
	search_fields = ('title', 'body')