from rest_framework import serializers

from repo.models import Repository


class RepositorySerializer(serializers.ModelSerializer):
    created_by_repr = serializers.StringRelatedField(source='created_by', read_only=True)

    class Meta:
        model = Repository
        fields = ['id', 'name', 'type', 'images_json', 'environment_config', 'created_by', 'created_by_repr', 'created_at']
