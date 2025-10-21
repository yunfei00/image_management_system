from django.db import models

# Create your models here.
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, verbose_name="报表类型")
    data = models.JSONField(verbose_name="报表数据")
    period = models.CharField(max_length=100, verbose_name="时间周期")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "报表"
        verbose_name_plural = "报表管理"
