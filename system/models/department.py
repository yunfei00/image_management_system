from .base_model import BaseModel
from django.db import models

class Department(BaseModel):
    name = models.CharField(max_length=64, verbose_name="部门名称")
    code = models.CharField(max_length=64, verbose_name="部门编码")
    leader = models.ForeignKey(
        'system.User',
        null=True,
        blank=True,
        related_name='managed_departments',
        on_delete=models.SET_NULL,
        verbose_name="负责人")

    class Meta:
        verbose_name = "部门管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name