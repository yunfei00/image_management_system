from django.db import models
from django.core.validators import MinValueValidator

class BaseImage(models.Model):
    name = models.CharField(max_length=255, verbose_name="镜像名称", db_index=True)
    version = models.CharField(max_length=100, verbose_name="版本", db_index=True)
    image_id = models.CharField(max_length=191, unique=True, verbose_name="镜像ID")  # 191 适配 MySQL utf8mb4
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    size = models.BigIntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="大小")
    status = models.CharField(max_length=50, default="草稿", verbose_name="状态", db_index=True)
    category = models.CharField(max_length=50, blank=True, default="", verbose_name="分类", db_index=True)
    description = models.TextField(blank=True, default="", verbose_name="描述")

    class Meta:
        verbose_name = "基础镜像"
        verbose_name_plural = "基础镜像管理"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["name", "version"], name="uniq_baseimage_name_version"),
        ]

    def __str__(self):
        return f"{self.name}:{self.version}"


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
