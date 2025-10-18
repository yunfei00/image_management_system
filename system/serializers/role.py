from rest_framework import serializers
from system.models import Permission, Role, RoleUser

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Permission.objects.all(), source='permissions', required=False)
    class Meta:
        model = Role
        fields = ['id','name','code','description','permissions','permission_ids','status','created_at']

class RoleUserSerializer(serializers.ModelSerializer):
    user_repr = serializers.StringRelatedField(source='user', read_only=True)
    role_repr = serializers.StringRelatedField(source='role', read_only=True)
    class Meta:
        model = RoleUser
        fields = ['id','user','user_repr','role','role_repr','assigned_at']