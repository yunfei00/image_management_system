from rest_framework import serializers
from system.models import OperationLog


class OperationLogSerializer(serializers.ModelSerializer):
    formatted_time = serializers.SerializerMethodField()
    class Meta:
        model = OperationLog
        fields = [
            'id',
            'module',
            'operator',
            'operation_time',
            'formatted_time',
            'ip',
            'operation_content',
        ]

    def get_formatted_time(self, obj):
        return obj.operation_time.strftime("%Y-%m-%d %H:%M:%S") if obj.operation_time else ""
