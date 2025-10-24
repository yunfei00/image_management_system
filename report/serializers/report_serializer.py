from rest_framework import serializers

from report.models import Report


class ReportSerializer(serializers.ModelSerializer):
    # 显示报表类型（选择值的显示）
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    # 如果需要更多的字段进行显示，可以在这里处理
    class Meta:
        model = Report
        fields = ['id', 'type', 'type_display', 'data', 'period', 'created_at', 'project_status', 'department', 'export_path']
