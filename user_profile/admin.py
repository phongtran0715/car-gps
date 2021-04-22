from django.contrib import admin
from user_profile.models import UserProfile
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.auth.models import User


class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile


class UserProfileAdmin(ImportExportActionModelAdmin):
    resource_class = UserProfileResource


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class MyUserAdmin(ImportExportActionModelAdmin):
    resource_class = UserResource


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
