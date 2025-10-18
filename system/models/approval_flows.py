from .base_model import BaseModel
from django.db import models

class ApprovalFlow(BaseModel):
    name = models.CharField(max_length=128)
    nodes_config = models.JSONField(default=list)  # list of nodes
    scope_type = models.CharField(max_length=32, default='global')
    scope_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'approval_flows'
    def __str__(self):
        return self.name