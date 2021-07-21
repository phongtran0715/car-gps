from django.contrib import admin
from rest_framework_simplejwt.state import User
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from user_profile.models import UserProfile


class ProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'Profile'
	fk_name = 'id'


class UserAdminResource(resources.ModelResource):
	class Meta:
		model = User
		exclude = ('password', 'user_permissions', 'is_superuser', 'groups', 'is_staff')
		export_order = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'last_login']


class UserAdmin(ImportExportActionModelAdmin):
	inlines = (ProfileInline, )
	resource_class = UserAdminResource
	list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'last_login']
	list_filter = ['username', 'email']

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
