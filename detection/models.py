from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class DetectTool(models.Model):
    name = models.CharField(max_length=255, verbose_name="工具名称")
    type = models.CharField(max_length=100, verbose_name="类型")
    api_url = models.URLField(max_length=255, verbose_name="API地址")
    config = models.JSONField(verbose_name="配置参数")
    status = models.CharField(max_length=50, verbose_name="状态")
    last_test_time = models.DateTimeField(verbose_name="最后测试时间")

    class Meta:
        verbose_name = "检测工具"
        verbose_name_plural = "检测工具管理"


class ProjectDetectTool(models.Model):
    class Status(models.IntegerChoices):
        DISABLED = 0, _('禁用')
        ENABLED  = 1, _('启用')

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        verbose_name=_('项目'),
        related_name='detect_tool_links'
    )
    detect_tool = models.ForeignKey(
        'system.DetectTool',
        on_delete=models.RESTRICT,
        verbose_name=_('检测工具'),
        related_name='project_links'
    )
    config = models.JSONField(_('工具配置（JSON）'))   # 见下方推荐结构
    status = models.PositiveSmallIntegerField(_('状态'),
                                              choices=Status.choices,
                                              default=Status.ENABLED)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        db_table = 'project_detect_tools'
        verbose_name = _('项目检测工具配置')
        verbose_name_plural = _('项目检测工具配置')
        constraints = [
            models.UniqueConstraint(fields=['project', 'detect_tool'],
                                    name='uk_project_tool'),
        ]
        indexes = [
            models.Index(fields=['project'], name='idx_project'),
            models.Index(fields=['detect_tool'], name='idx_tool'),
            models.Index(fields=['status'], name='idx_status'),
        ]

    def __str__(self):
        return f'{self.project_id} - {self.detect_tool_id}'


class PreDetectionRecord(models.Model):
    class Status(models.IntegerChoices):
        PENDING    = 1, _('待检测')
        IN_PROGRESS = 2, _('检测中')
        COMPLETED  = 3, _('已完成')
        FAILED     = 4, _('已失败')

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        verbose_name=_('项目'),
        related_name='pre_detection_records'
    )
    tool = models.ForeignKey(
        'system.DetectTool',
        on_delete=models.RESTRICT,
        verbose_name=_('检测工具'),
        related_name='pre_detection_records'
    )
    status = models.PositiveSmallIntegerField(_('状态'), choices=Status.choices, default=Status.PENDING)
    report_path = models.CharField(_('报告路径'), max_length=255, null=True, blank=True)
    vulnerability_count = models.IntegerField(_('漏洞数量'), default=0)
    detect_time = models.DateTimeField(_('检测时间'), auto_now_add=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        db_table = 'pre_detect_records'
        verbose_name = _('预检测记录')
        verbose_name_plural = _('预检测记录管理')
        indexes = [
            models.Index(fields=['project'], name='idx_project'),
            models.Index(fields=['tool'], name='idx_tool'),
            models.Index(fields=['status'], name='idx_status'),
            models.Index(fields=['vulnerability_count'], name='idx_vulnerability_count'),
        ]

    def __str__(self):
        return f'{self.project} - {self.tool} ({self.get_status_display()})'


# apps/security/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class SecurityDetectionApplication(models.Model):
    class Status(models.IntegerChoices):
        PENDING    = 1, _('待检测')
        IN_PROGRESS = 2, _('检测中')
        COMPLETED  = 3, _('已完成')
        FAILED     = 4, _('已失败')

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        verbose_name=_('项目'),
        related_name='security_detection_applications'
    )
    file_paths = models.JSONField(_('文件路径'))
    detect_items = models.JSONField(_('检测项'))
    description = models.CharField(_('检测描述'), max_length=255, null=True, blank=True)
    assign_team = models.CharField(_('指定检测团队'), max_length=255, null=True, blank=True)
    status = models.PositiveSmallIntegerField(_('状态'), choices=Status.choices, default=Status.PENDING)
    result = models.CharField(_('检测结果'), max_length=255, null=True, blank=True)
    feedback = models.TextField(_('检测反馈'), null=True, blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        db_table = 'security_detect_apply'
        verbose_name = _('安全检测申请')
        verbose_name_plural = _('安全检测申请管理')
        indexes = [
            models.Index(fields=['project'], name='idx_project'),
            models.Index(fields=['status'], name='idx_status'),
        ]

    def __str__(self):
        return f'{self.project} - {self.get_status_display()}'
