from .base_model import BaseModel
from django.db import models
from django.conf import settings

class Permission(models.Model):
    """最小权限单元，用点号命名空间，例如：image.view, image.upload"""
    key = models.CharField(max_length=128, unique=True, verbose_name="权限键")
    name = models.CharField(max_length=128, verbose_name="权限名称")
    description = models.TextField(blank=True, null=True, verbose_name="描述")

    class Meta:
        db_table = 'permissions'
        verbose_name = '权限'
        verbose_name_plural = '权限管理'

    def __str__(self):
        return self.key


class Role(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name="角色名称")
    code = models.CharField(max_length=64, unique=True, verbose_name="权限标识")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='roles',
        verbose_name='权限集合')

    class Meta:
        db_table = 'roles'
        verbose_name = '角色'
        verbose_name_plural = '角色管理'

    def __str__(self):
        return f"{self.name} ({self.code})"


class RoleUser(models.Model):
    """用户与角色的关联（一个用户可以有多个角色）"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='role_links'
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='user_links'
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role_user'
        unique_together = ('user', 'role')
        verbose_name = '用户角色关联'
        verbose_name_plural = '用户角色关联'

    def __str__(self):
        return f"{self.user} -> {self.role}"