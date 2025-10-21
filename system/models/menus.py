from .base_model import BaseModel
from django.db import models

# Menus
# apps/system/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class Menu(models.Model):
    class Status(models.IntegerChoices):
        DISABLED = 0, _('禁用')
        ENABLED  = 1, _('启用')

    name = models.CharField(_('菜单名称'), max_length=64)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        verbose_name=_('父菜单'), related_name='children'
    )
    path = models.CharField(_('菜单路径'), max_length=255)
    icon = models.CharField(_('图标'), max_length=64, null=True, blank=True)
    sort = models.IntegerField(_('排序'), default=0)
    status = models.PositiveSmallIntegerField(_('状态'), choices=Status.choices, default=Status.ENABLED)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        db_table = 'menus'
        verbose_name = _('菜单')
        verbose_name_plural = _('菜单管理')
        indexes = [
            models.Index(fields=['status'], name='idx_status'),
            models.Index(fields=['sort'], name='idx_sort'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['parent', 'name'], name='uk_parent_name'),
        ]

    def __str__(self):
        return self.name


