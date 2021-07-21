from django.contrib import admin
from .models import UserProfile
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin



class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile

class UserProfileAdmin(ImportExportActionModelAdmin):
    resource_class = UserProfileResource
    list_display = ['id', 'car_name', 'plate_number', 'avatar']
    list_filter = ['id', 'plate_number']


admin.site.register(UserProfile, UserProfileAdmin)
