# system/serializers/login_log_serializer.py
from rest_framework import serializers
from system.models.login_log import LoginLog


class LoginLogSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    formatted_time = serializers.SerializerMethodField()

    class Meta:
        model = LoginLog
        fields = [
            'id',
            'username',
            'ip',
            'status',
            'status_display',
            'result',
            'login_time',
            'formatted_time',
        ]

    # status_display：让前端更直观地看到中文结果
    # ✅ formatted_time：输出美观的时间字符串

    def get_status_display(self, obj):
        return "成功" if obj.status else "失败"

    def get_formatted_time(self, obj):
        return obj.login_time.strftime("%Y-%m-%d %H:%M:%S") if obj.login_time else ""
