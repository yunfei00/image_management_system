from django.db import models
from django.core.validators import MinValueValidator

class BaseImage(models.Model):
    class Status(models.IntegerChoices):
        DISABLED = 0, '禁用'
        ENABLED  = 1, '启用'
        DRAFT    = 2, '草稿'

    class Category(models.TextChoices):
        OS = 'os', '操作系统'
        MIDDLEWARE = 'middleware', '中间件'
        JDK = 'jdk', 'JDK'
        OTHER = 'other', '其他'
    name = models.CharField(max_length=255, verbose_name="镜像名称", db_index=True)
    version = models.CharField(max_length=100, verbose_name="版本", db_index=True)
    image_id = models.CharField(max_length=191, unique=True, verbose_name="镜像ID")  # 191 适配 MySQL utf8mb4
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    size = models.BigIntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="大小")
    status = models.IntegerField(choices=Status.choices, default=Status.ENABLED, verbose_name="状态", db_index=True)
    category = models.CharField(max_length=50, blank=True, default="", verbose_name="分类", db_index=True)
    description = models.TextField(blank=True, default="", verbose_name="描述")

    # 下载相关：可存本地/NFS 相对路径，或对象存储(OSS/MinIO/S3)的 Key
    artifact_path = models.CharField(max_length=255, blank=True, default="", verbose_name="镜像包路径")
    # 部门可见性：为空表示全员可见；否则取交集
    visible_departments = models.JSONField(default=list, blank=True, verbose_name="可见部门编码列表")

    class Meta:
        verbose_name = "基础镜像"
        verbose_name_plural = "基础镜像管理"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["name", "version"], name="uniq_baseimage_name_version"),
        ]

        permissions = [
            ("image_download", "下载基础镜像"),
            ("image_upload", "上传基础镜像"),
            ("image_delete_hard", "物理删除基础镜像"),
        ]

    def __str__(self):
        return f"{self.name}:{self.version}"

    @property
    def size_human(self):
        s = self.size or 0
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if s < 1024:
                return f"{s:.1f}{unit}"
            s /= 1024
        return f"{s:.1f}EB"


class BusinessImage(models.Model):
    name = models.CharField(max_length=255, verbose_name="镜像名称", db_index=True)
    version = models.CharField(max_length=100, verbose_name="版本", db_index=True)
    image_id = models.CharField(max_length=191, unique=True, verbose_name="镜像ID")
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, verbose_name="项目", related_name="business_images")
    detect_status = models.CharField(max_length=50, default="待检测", verbose_name="检测状态", db_index=True)
    approve_status = models.CharField(max_length=50, default="无需", verbose_name="审批状态", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    size = models.BigIntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="大小")

    class Meta:
        verbose_name = "业务镜像"
        verbose_name_plural = "业务镜像管理"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["project", "detect_status"]),
        ]

    def __str__(self):
        return f"{self.name}:{self.version}"
