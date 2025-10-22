# images/serializers.py
from rest_framework import serializers
from .models import BaseImage, BusinessImage

class BaseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseImage
        fields = [
            'id', 'name', 'version', 'image_id',
            'size', 'status', 'category', 'description',
            'created_at',
        ]


class BusinessImageSerializer(serializers.ModelSerializer):
    # 只读的人类可读展示（依赖 Project.__str__）
    project_repr = serializers.StringRelatedField(source='project', read_only=True)

    class Meta:
        model = BusinessImage
        fields = [
            'id', 'name', 'version', 'image_id',
            'project', 'project_repr',
            'detect_status', 'approve_status',
            'size', 'created_at',
        ]
