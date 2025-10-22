# projects/serializers/project.py
from rest_framework import serializers
from projects.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    # 便于前端直接显示人类可读值
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    # approval_status_display = serializers.CharField(source="get_approval_status_display", read_only=True)
    applicant_repr = serializers.StringRelatedField(source="applicant", read_only=True)
    department_repr = serializers.StringRelatedField(source="department", read_only=True)
    base_image_repr = serializers.StringRelatedField(source="base_image", read_only=True)
    # approval_flow_repr = serializers.StringRelatedField(source="approval_flow", read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "code", "name",
            "applicant", "applicant_repr",
            "department", "department_repr",
            "end_user", "description",
            "plan_online_date",
            "base_image", "base_image_repr",
            "components",
            "status", "status_display",
            # "approval_status", "approval_status_display",
            # "approval_flow", "approval_flow_repr",
            "submit_at", "updated_at",
        ]
        read_only_fields = ["submit_at", "updated_at"]
