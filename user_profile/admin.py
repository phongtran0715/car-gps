from django.contrib import admin
from user_profile.models import UserProfile
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile


class UserProfileAdmin(ImportExportActionModelAdmin):
    resource_class = UserProfileResource


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
