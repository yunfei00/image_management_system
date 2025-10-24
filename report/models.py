
from django.db import models

from system.models.base_model import BaseModel


class Report(BaseModel):
    class ReportType(models.TextChoices):
        PROJECT = "PROJECT", "项目报表"
        IMAGE = "IMAGE", "镜像报表"
        BUSINESS_IMAGE = "BUSINESS_IMAGE", "业务镜像报表"
        BUSINESS_PROCESS = "BUSINESS_PROCESS", "业务流程报表"

    # 报表类型
    type = models.CharField(
        max_length=64,
        choices=ReportType.choices,
        verbose_name="报表类型"
    )

    # 报表数据，以JSON格式存储报表内容
    data = models.JSONField(verbose_name="报表数据")

    # 统计的时间范围
    period = models.CharField(max_length=64, verbose_name="时间段")

    # 创建时间，自动生成
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    # 可选的附加字段，如：项目状态、部门等，用于筛选
    project_status = models.CharField(max_length=64, blank=True, null=True, verbose_name="项目状态")
    department = models.CharField(max_length=64, blank=True, null=True, verbose_name="部门")

    # 导出文件路径，可能用于存储生成的PDF/Excel文件
    export_path = models.CharField(max_length=256, blank=True, null=True, verbose_name="导出路径")

    class Meta:
        verbose_name = "报表管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_type_display()} - {self.period}"
