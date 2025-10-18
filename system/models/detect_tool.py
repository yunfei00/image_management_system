from .base_model import BaseModel
from django.db import models

# Detect Tools
class DetectTool(BaseModel):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=64)  # e.g., green, xiaoyou
    api_url = models.URLField()
    config = models.JSONField(default=dict, blank=True)
    last_test_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'detect_tools'
    def __str__(self):
        return self.name