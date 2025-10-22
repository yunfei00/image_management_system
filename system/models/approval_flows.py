# apps/approvals/models.py
from django.db import models
from .base_model import BaseModel  # 与 Department 一致的继承方式

class ApprovalFlow(BaseModel):
    """审批流程配置"""
    class Status(models.IntegerChoices):
        DISABLED = 0, "禁用"
        ENABLED  = 1, "启用"

    name = models.CharField(max_length=64, unique=True, db_index=True, verbose_name="流程名称")
    nodes_config = models.JSONField(verbose_name="审批节点配置")  # 前端以 JSON 编辑/保存
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.ENABLED, db_index=True, verbose_name="状态"
    )

    class Meta:
        db_table = "approval_flows"             # 与需求表名一致
        verbose_name = "审批流程"
        verbose_name_plural = "审批流程配置"
        ordering = ("-created_at", "id")        # 列表默认按创建时间倒序

    def __str__(self):
        return self.name
