from django.contrib import admin
from .models import Role, Permission, RoleUser

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