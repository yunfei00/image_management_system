# from django.db import models
# from django.utils.translation import gettext_lazy as _
#
# class Repository(models.Model):
#     name = models.CharField(_('仓库名称'), max_length=64)
#     type = models.CharField(_('仓库类型'), max_length=32)
#     images_json = models.JSONField(_('镜像列表（JSON）'))
#     environment_config = models.JSONField(_('环境配置'))
#     created_by = models.ForeignKey(
#         'system.User',
#         on_delete=models.CASCADE,
#         verbose_name=_('创建者'),
#         related_name='created_repositories'
#     )
#     created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
#     updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
#
#     class Meta:
#         db_table = 'repositories'
#         verbose_name = _('仓库')
#         verbose_name_plural = _('仓库管理')
#         indexes = [
#             models.Index(fields=['name'], name='idx_name'),
#             models.Index(fields=['type'], name='idx_type'),
#             models.Index(fields=['created_by'], name='idx_created_by'),
#         ]
#
#     def __str__(self):
#         return self.name
