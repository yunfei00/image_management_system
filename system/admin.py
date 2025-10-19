from django.contrib import admin
from .models import Role, Permission, RoleUser, LoginLog


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'name')
    search_fields = ('key', 'name')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'status', 'created_at')
    search_fields = ('name', 'code')
    filter_horizontal = ('permissions',)

@admin.register(RoleUser)
class RoleUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'assigned_at')
    search_fields = ('user__username', 'role__name')

@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ('username', 'login_time', 'ip', 'status', 'result')
    list_filter = ('status', 'login_time')
    search_fields = ('username', 'ip', 'result')
    ordering = ('-login_time',)