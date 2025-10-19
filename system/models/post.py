from .base_model import BaseModel
from django.db import models

class Position(BaseModel):
    """职位表（如：前端开发、产品经理）"""
    name = models.CharField(max_length=64, verbose_name="岗位名称")
    code = models.CharField(max_length=50, unique=True, verbose_name='岗位编码')
    description = models.TextField(blank=True, null=True, verbose_name='描述')

    class Meta:
        db_table = 'positions'
        verbose_name = '岗位管理'
        verbose_name_plural = '岗位管理'

    def __str__(self):
        return self.name
