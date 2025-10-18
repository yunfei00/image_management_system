from rest_framework import serializers
from django.contrib.auth import get_user_model
from system.models import (Permission, Role, RoleUser, Department, Position, DetectTool,
                     LoginLog, OperationLog, Menu, ApprovalFlow)

User = get_user_model()

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

class DepartmentSerializer(serializers.ModelSerializer):
    leader_repr = serializers.StringRelatedField(source='leader', read_only=True)
    class Meta:
        model = Department
        fields = ['id','name','code','leader','leader_repr','status','created_at']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class DetectToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectTool
        fields = '__all__'

class LoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = '__all__'

class OperationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationLog
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class ApprovalFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalFlow
        fields = '__all__'

# User serializer for admin APIs
class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','username','email','is_active','roles']
    def get_roles(self,obj):
        return [r.role.code for r in obj.role_links.all()]