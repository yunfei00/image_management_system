from rest_framework import serializers
from system.models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    leader_repr = serializers.StringRelatedField(source='leader', read_only=True)
    class Meta:
        model = Department
        fields = ['id','name','code','leader','leader_repr','status','created_at']