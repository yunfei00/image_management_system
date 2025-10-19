from django.db import models

class LoginLog(models.Model):
    STATUS_CHOICES = (
        ('success', '成功'),
        ('fail', '失败'),
    )

    username = models.CharField(max_length=50, verbose_name="用户名")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="登录时间")
    ip = models.GenericIPAddressField(verbose_name="登录IP", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="状态")
    result = models.TextField(verbose_name="登录结果", null=True, blank=True)

    class Meta:
        db_table = "login_logs"
        verbose_name = "登录日志"
        verbose_name_plural = "登录日志"
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.username} - {self.status}"
