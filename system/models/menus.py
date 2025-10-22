from __future__ import annotations
from django.db import models
from django.contrib.auth.models import Group

class Menu(models.Model):
    class Status(models.IntegerChoices):
        DISABLED = 0, '禁用'
        ENABLED  = 1, '启用'

    name = models.CharField('菜单名称', max_length=64)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE, verbose_name='父菜单'
    )
    path = models.CharField('菜单路径', max_length=255, unique=True,
                            help_text='前端路由或后端URL；外链可填完整URL')
    icon = models.CharField('图标', max_length=64, blank=True, default='')
    sort = models.PositiveIntegerField('排序', default=0)
    status = models.PositiveSmallIntegerField('状态',
                                              choices=Status.choices,
                                              default=Status.ENABLED)
    visible = models.BooleanField('是否显示', default=True)
    is_external = models.BooleanField('是否外链', default=False)
    permission = models.CharField(
        '权限标识', max_length=128, blank=True, default='',
        help_text='用于前端/后端细粒度权限控制，可留空'
    )
    groups = models.ManyToManyField(
        Group, blank=True, related_name='menus', verbose_name='可见用户组'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = '菜单'
        ordering = ['sort', 'id']
        constraints = [
            models.UniqueConstraint(fields=['parent', 'name'], name='uniq_parent_name')
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def is_enabled(self) -> bool:
        return self.status == self.Status.ENABLED
