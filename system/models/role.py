from .base_model import BaseModel
from django.db import models


class Role(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name="角色名称")
    code = models.CharField(max_length=64, unique=True, verbose_name="角色编码")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    permission_keys = models.JSONField(default=list, verbose_name="权限Key列表")
    permissions = models.JSONField(default=dict, verbose_name="权限结构")

    class Meta:
        db_table = "system_role"
        verbose_name = "角色"
        verbose_name_plural = "角色管理"

    def __str__(self):
        return self.name