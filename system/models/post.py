from .base_model import BaseModel
from django.db import models

class Position(BaseModel):
    """职位表（如：前端开发、产品经理）"""
    name = models.CharField(max_length=64, verbose_name="职位名称")
    department = models.ForeignKey(
        'system.Department',
        on_delete=models.CASCADE,
        related_name="positions",
        verbose_name="所属部门")

    class Meta:
        verbose_name = "职位"
        verbose_name_plural = "职位"
        unique_together = ("name", "department")  # 同一部门内职位名称唯一

    def __str__(self):
        return f"{self.department.name}-{self.name}"