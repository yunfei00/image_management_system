from rest_framework import serializers

from detection.models import DetectTool


class DetectToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectTool
        fields = ["id","name","type","api_url","config","status","last_test_time","created_at"]
