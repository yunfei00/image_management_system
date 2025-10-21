from django.db import models

# Create your models here.
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.TextField(verbose_name="通知内容")
    type = models.CharField(max_length=50, verbose_name="通知类型")
    status = models.CharField(max_length=50, verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "通知消息"
        verbose_name_plural = "通知消息管理"

