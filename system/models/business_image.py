from django.db import models


class BusinessImage(models.Model):
    name = models.CharField(max_length=255, verbose_name="镜像名称")
    version = models.CharField(max_length=100, verbose_name="版本")
    image_id = models.CharField(max_length=100, verbose_name="镜像ID")
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name="项目")
    detect_status = models.CharField(max_length=50, verbose_name="检测状态")
    approve_status = models.CharField(max_length=50, verbose_name="审批状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    size = models.IntegerField(verbose_name="大小")

    class Meta:
        verbose_name = "业务镜像"
        verbose_name_plural = "业务镜像管理"