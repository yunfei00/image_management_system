from .base_model import BaseModel
from django.db import models

# Menus
class Menu(BaseModel):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    path = models.CharField(max_length=256, blank=True, null=True)
    icon = models.CharField(max_length=64, blank=True, null=True)
    sort = models.IntegerField(default=0)
    meta = models.JSONField(default=dict, blank=True)  # e.g., {title, permission_key}
    class Meta:
        db_table = 'menus'
    def __str__(self):
        return self.name