from rest_framework import serializers
from detection.models import DetectCenterConfig, DetectDevice

class DetectCenterConfigSerializer(serializers.ModelSerializer):
    approval_flow_name = serializers.CharField(source='approval_flow.name', read_only=True)

    class Meta:
        model = DetectCenterConfig
        fields = [
            'id', 'name', 'api_config', 'approval_flow', 'approval_flow_name',
            'device_config', 'status', 'created_at'
        ]

class DetectDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectDevice
        fields = ['id', 'name', 'type', 'api_url', 'config', 'status', 'created_at']
