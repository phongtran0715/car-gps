from django.contrib import admin
from rest_framework_simplejwt.state import User
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class UserAdminResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('password', 'user_permissions')


class UserAdmin(ImportExportActionModelAdmin):
	resource_class = UserAdminResource


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
