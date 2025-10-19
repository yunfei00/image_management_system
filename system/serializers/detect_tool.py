from rest_framework import serializers
from system.models import DetectTool

class DetectToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectTool
        fields = '__all__'