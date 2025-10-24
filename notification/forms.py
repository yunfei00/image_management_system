# notifications/forms.py
from django import forms

from notification.models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'type', 'level', 'title', 'content', 'link_url', 'status']
