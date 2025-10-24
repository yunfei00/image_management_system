# notifications/serializers/notification.py
from rest_framework import serializers

from notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    user_repr = serializers.StringRelatedField(source='user', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_repr',
            'type', 'status', 'level',
            'title', 'content', 'link_url', 'extra',
            'created_at', 'read_at'
        ]
