from rest_framework import serializers

from detection.models import SecurityDetectApply


class SecurityDetectApplySerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    leader_name = serializers.StringRelatedField(source='assign_team', read_only=True)

    class Meta:
        model = SecurityDetectApply
        fields = ['id', 'project', 'project_name', 'file_paths', 'detect_items', 'description', 'assign_team', 'leader_name', 'status', 'result', 'feedback', 'created_at']
