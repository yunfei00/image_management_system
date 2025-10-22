from django.db import models


# Create your models here.
class DetectTool(models.Model):
    name = models.CharField(max_length=255, verbose_name="工具名称")
    type = models.CharField(max_length=100, verbose_name="类型")
    api_url = models.URLField(max_length=255, verbose_name="API地址")
    config = models.JSONField(verbose_name="配置参数")
    status = models.CharField(max_length=50, verbose_name="状态")
    last_test_time = models.DateTimeField(verbose_name="最后测试时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "检测工具"
        verbose_name_plural = "检测工具管理"


class ProjectDetectTool(models.Model):
    class Status(models.IntegerChoices):
        DISABLED = 0, '禁用'
        ENABLED  = 1, '启用'

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        verbose_name='项目',
        related_name='detect_tool_links'
    )
    detect_tool = models.ForeignKey(
        DetectTool,
        on_delete=models.RESTRICT,
        verbose_name='检测工具',
        related_name='project_links'
    )
    config = models.JSONField('工具配置（JSON）')   # 见下方推荐结构
    status = models.PositiveSmallIntegerField('状态',
                                              choices=Status.choices,
                                              default=Status.ENABLED)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'project_detect_tools'
        verbose_name = '项目检测工具配置'
        verbose_name_plural = '项目检测工具配置'
        constraints = [
            models.UniqueConstraint(fields=['project', 'detect_tool'],
                                    name='uk_project_tool'),
        ]
        # indexes = [
        #     models.Index(fields=['project'], name='idx_project'),
        #     models.Index(fields=['detect_tool'], name='idx_tool'),
        #     models.Index(fields=['status'], name='idx_status'),
        # ]

    def __str__(self):
        return f'{self.project_id} - {self.detect_tool_id}'


class PreDetectionRecord(models.Model):
    class Status(models.IntegerChoices):
        PENDING    = 1, '待检测'
        IN_PROGRESS = 2, '检测中'
        COMPLETED  = 3, '已完成'
        FAILED     = 4, '已失败'

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        verbose_name='项目',
        related_name='pre_detection_records'
    )
    tool = models.ForeignKey(
        DetectTool,
        on_delete=models.RESTRICT,
        verbose_name='检测工具',
        related_name='pre_detection_records'
    )
    status = models.PositiveSmallIntegerField('状态', choices=Status.choices, default=Status.PENDING)
    report_path = models.CharField('报告路径', max_length=255, null=True, blank=True)
    vulnerability_count = models.IntegerField('漏洞数量', default=0)
    detect_time = models.DateTimeField('检测时间', auto_now_add=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'pre_detect_records'
        verbose_name = '预检测记录'
        verbose_name_plural = '预检测记录管理'

    def __str__(self):
        return f'{self.project} - {self.tool} ({self.get_status_display()})'


class SecurityDetectionApplication(models.Model):
    class Status(models.IntegerChoices):
        PENDING    = 1, '待检测'
        IN_PROGRESS = 2, '检测中'
        COMPLETED  = 3, '已完成'
        FAILED     = 4, '已失败'

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        verbose_name='项目',
        related_name='security_detection_applications'
    )
    file_paths = models.JSONField('文件路径')
    detect_items = models.JSONField('检测项')
    description = models.CharField('检测描述', max_length=255, null=True, blank=True)
    assign_team = models.CharField('指定检测团队', max_length=255, null=True, blank=True)
    status = models.PositiveSmallIntegerField('状态', choices=Status.choices, default=Status.PENDING)
    result = models.CharField('检测结果', max_length=255, null=True, blank=True)
    feedback = models.TextField('检测反馈', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'security_detect_apply'
        verbose_name = '安全检测申请'
        verbose_name_plural = '安全检测申请管理'
        # indexes = [
        #     models.Index(fields=['project'], name='idx_project'),
        #     models.Index(fields=['status'], name='idx_status'),
        # ]

    def __str__(self):
        return f'{self.project} - {self.get_status_display()}'
