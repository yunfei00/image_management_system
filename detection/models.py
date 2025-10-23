from django.db import models

from system.models.base_model import BaseModel


class DetectTool(BaseModel):
    """检测工具管理（供项目选择）"""
    class Status(models.IntegerChoices):
        DISABLED = 0, "禁用"
        ENABLED  = 1, "启用"

    class Type(models.TextChoices):
        STATIC_CODE = "STATIC_CODE", "静态代码扫描"
        IMAGE_VULN  = "IMAGE_VULN",  "镜像漏洞扫描"
        SCA         = "SCA",         "依赖成分分析"
        LICENSE     = "LICENSE",     "许可证合规"
        DAST        = "DAST",        "动态安全测试"

    name = models.CharField(max_length=64, unique=True, verbose_name="工具名称")
    type = models.CharField(max_length=32, choices=Type.choices, verbose_name="工具类型")
    api_url = models.URLField(verbose_name="服务地址")
    config = models.JSONField(default=dict, blank=True, verbose_name="默认配置")
    status = models.IntegerField(choices=Status.choices, default=Status.ENABLED, verbose_name="状态")
    last_test_time = models.DateTimeField(null=True, blank=True, verbose_name="最近连通时间")

    class Meta:
        db_table = "detect_tools"
        verbose_name = "检测工具管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProjectDetectTool(BaseModel):
    """项目-检测工具 关联（检测策略项）"""
    class Availability(models.IntegerChoices):
        UNKNOWN = 0, "未知"
        OK      = 1, "可用"
        FAIL    = 2, "不可用"

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="detect_strategy", verbose_name="项目")
    tool = models.ForeignKey(
        DetectTool, on_delete=models.PROTECT, related_name="project_bindings", verbose_name="检测工具")
    config = models.JSONField(default=dict, blank=True, verbose_name="项目级配置")
    available = models.IntegerField(choices=Availability.choices, default=Availability.UNKNOWN, verbose_name="可用性")

    class Meta:
        db_table = "project_detect_tools"
        verbose_name = "项目检测工具策略"
        verbose_name_plural = verbose_name
        unique_together = [("project", "tool")]
        indexes = [models.Index(fields=["project", "tool"])]

    def __str__(self):
        return f"{self.project} - {self.tool}"


class PreDetectRecord(BaseModel):
    """预检测记录（由 SDK/CI 触发的异步检测）"""
    class Status(models.TextChoices):
        PENDING  = "PENDING",  "排队中"
        RUNNING  = "RUNNING",  "检测中"
        SUCCESS  = "SUCCESS",  "成功"
        FAILED   = "FAILED",   "失败"
        TIMEOUT  = "TIMEOUT",  "超时"
        CANCELED = "CANCELED", "已取消"

    project = models.ForeignKey(
        "projects.Project", on_delete=models.PROTECT, related_name="pre_detects", verbose_name="项目")
    tool = models.ForeignKey(
        DetectTool, on_delete=models.PROTECT, related_name="pre_detects", verbose_name="检测工具")
    request_id = models.CharField(max_length=64, blank=True, default="", verbose_name="幂等请求ID")
    payload = models.JSONField(default=dict, verbose_name="检测请求载荷")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, verbose_name="状态")
    report_path = models.CharField(max_length=512, blank=True, default="", verbose_name="报告路径")
    vulnerability_count = models.IntegerField(default=0, verbose_name="漏洞数量")
    error_message = models.TextField(blank=True, default="", verbose_name="错误信息")
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="开始时间")
    detect_time = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    rerun_of = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="重跑来源")

    class Meta:
        db_table = "pre_detect_records"
        verbose_name = "预检测记录"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["project", "tool", "status"]),
            models.Index(fields=["request_id"]),
        ]

    def __str__(self):
        return f"{self.project} - {self.tool} - {self.get_status_display()}"
