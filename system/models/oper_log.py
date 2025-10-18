from django.conf import settings
from django.db import models

class OperationLog(models.Model):
    module = models.CharField(max_length=128)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    operator_name = models.CharField(max_length=150, blank=True, null=True)
    operation_time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=64, blank=True, null=True)
    operation_content = models.TextField()
    request_path = models.CharField(max_length=256, blank=True, null=True)
    method = models.CharField(max_length=8, blank=True, null=True)
    class Meta:
        db_table = 'operation_logs'