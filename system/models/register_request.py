# system/models/register_request.py
from django.db import models
from system.models import User, Position
from .role import Role

class RegisterRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审批'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )

    name = models.CharField(max_length=64, verbose_name="姓名")
    phone = models.CharField(max_length=20, unique=True, verbose_name="电话")
    company = models.CharField(max_length=128, verbose_name="公司名称")
    position =  models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, verbose_name="申请岗位")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, verbose_name="申请角色")
    password = models.CharField(max_length=128, verbose_name="密码")  # ✅ 新增字段
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="审批状态")
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_requests', verbose_name="审批人")
    comment = models.TextField(blank=True, verbose_name="审批意见")

    class Meta:
        verbose_name = "注册申请"
        verbose_name_plural = "注册申请"

    def __str__(self):
        return f"{self.name}（{self.phone}）"
