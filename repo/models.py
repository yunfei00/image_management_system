from django.db import models

from system.models.base_model import BaseModel


class Repository(BaseModel):
    name = models.CharField(max_length=128, verbose_name="仓库名称", unique=True)
    type = models.CharField(max_length=64, verbose_name="仓库类型", choices=[('system', '系统'), ('test', '测试'), ('production', '生产')])
    images_json = models.JSONField(verbose_name="镜像信息", help_text="存储仓库中镜像的 JSON 数据")
    environment_config = models.JSONField(verbose_name="环境配置", help_text="不同环境的配置，系统、测试、生产")
    created_by = models.ForeignKey(
        'system.User',
        null=True,
        blank=True,
        related_name='created_repositories',
        on_delete=models.SET_NULL,
        verbose_name="创建者"
    )

    class Meta:
        verbose_name = "仓库管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
