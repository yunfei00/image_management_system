from rest_framework import serializers

from detection.models import PreDetectRecord


class PreDetectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreDetectRecord
        fields = ["project","tool","payload","request_id"]

class PreDetectSerializer(serializers.ModelSerializer):
    project_repr = serializers.StringRelatedField(source="project", read_only=True)
    tool_repr = serializers.StringRelatedField(source="tool", read_only=True)

    class Meta:
        model = PreDetectRecord
        fields = "__all__"
