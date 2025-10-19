from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # 显示外键对象的名称，而不是 id
    role_name = serializers.CharField(source='role.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'phone',
            'company',
            'department', 'department_name',
            'role', 'role_name',
            'position', 'position_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
            'created_at',  # 来自 BaseModel
            'updated_at',  # 来自 BaseModel
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'created_at', 'updated_at']
