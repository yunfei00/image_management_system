from django.contrib.auth.models import AbstractUser

from .base_model import BaseModel
from django.db import models

class User(AbstractUser, BaseModel):
    # 复用AbstractUser的字段：id、password、email（已包含，可扩展约束）
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="用户名称",  # 显示别名，在Admin或表单中会显示“登录名”
        help_text="用于登录的账号，需唯一",
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="手机号")
    company = models.CharField(max_length=200, blank=True, null=True, verbose_name="公司名称")  # ← 新增字段
    department = models.ForeignKey(
        'system.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',  # 反向查询：通过部门查询其下所有用户
        verbose_name="所属部门")

    # 外键关联（对应role_id、department_id、position_id）
    role  = models.ForeignKey(
        'system.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="角色"
    )
    position = models.ForeignKey(
        'system.Position',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="职位"
    )

    # 覆盖内置email字段（可选，增强约束）
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户管理"

    def __str__(self):
        return self.username