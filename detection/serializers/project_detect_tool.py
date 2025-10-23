from rest_framework import serializers

from detection.models import DetectTool, ProjectDetectTool


class ProjectDetectToolSerializer(serializers.ModelSerializer):
    tool = serializers.StringRelatedField(read_only=True)
    tool_id = serializers.PrimaryKeyRelatedField(
        source="tool", queryset=DetectTool.objects.all(), write_only=True
    )
    project_repr = serializers.StringRelatedField(source="project", read_only=True)

    class Meta:
        model = ProjectDetectTool
        fields = [
            "id","project","project_repr","tool","tool_id","config",
            "available","created_at","updated_at"
        ]
