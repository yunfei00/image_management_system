from django.db import models


class LoginLog(models.Model):
    username = models.CharField(max_length=255, verbose_name="用户名")
    login_time = models.DateTimeField(verbose_name="登录时间")
    ip = models.CharField(max_length=50, verbose_name="登录IP")
    status = models.CharField(max_length=50, verbose_name="状态")
    result = models.CharField(max_length=50, verbose_name="登录结果")

    class Meta:
        db_table = "login_logs"
        verbose_name = "登录日志"
        verbose_name_plural = "登录日志管理"
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.username} - {self.status}"

class OperationLog(models.Model):
    module = models.CharField(max_length=255, verbose_name="系统模块")
    operator = models.CharField(max_length=255, verbose_name="操作人员")
    operation_time = models.DateTimeField(verbose_name="操作时间")
    ip = models.GenericIPAddressField("操作IP", null=True, blank=True, db_index=True)
    operation_content = models.TextField(verbose_name="操作内容")

    class Meta:
        db_table = "operation_logs"
        verbose_name = "操作日志"
        verbose_name_plural = "操作日志"
        ordering = ("-operation_time",)

    def __str__(self):
        return f"{self.operation_time} - {self.module} - {self.operator}"

