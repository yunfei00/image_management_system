from django.conf import settings
from django.db import models

# Logs
class LoginLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    username = models.CharField(max_length=150)
    login_time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=64, blank=True, null=True)
    status = models.BooleanField(default=True)
    result = models.TextField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'login_logs'