from rest_framework import serializers
from django.contrib.auth import get_user_model
from system.models import (Permission, Role, RoleUser, Department, Position, DetectTool,
                     LoginLog, OperationLog, Menu, ApprovalFlow)

User = get_user_model()


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