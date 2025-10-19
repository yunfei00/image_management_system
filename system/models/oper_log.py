from django.db import models


class OperationLog(models.Model):
    """
    操作日志表
    """
    module = models.CharField("系统模块", max_length=128, db_index=True)
    operator = models.CharField("操作人员", max_length=64, db_index=True)
    operation_time = models.DateTimeField("操作时间", auto_now_add=True, db_index=True)
    ip = models.GenericIPAddressField("操作IP", null=True, blank=True, db_index=True)
    operation_content = models.TextField("操作内容")

    class Meta:
        db_table = "operation_logs"
        verbose_name = "操作日志"
        verbose_name_plural = "操作日志"
        ordering = ("-operation_time",)

    def __str__(self):
        return f"{self.operation_time} - {self.module} - {self.operator}"
