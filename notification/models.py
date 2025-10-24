# notifications/models.py
from django.db import models
from django.db.models import Q

from system.models.base_model import BaseModel


class Notification(BaseModel):
    """
    单用户消息。广播时建议做“扇出”：为每个接收人生成一条记录，以便独立管理阅读状态。
    """
    class Type(models.TextChoices):
        APPROVAL = "APPROVAL", "审批通知"
        DETECT   = "DETECT",   "检测通知"
        SYSTEM   = "SYSTEM",   "系统通知"

    class Status(models.TextChoices):
        UNREAD   = "UNREAD",   "未读"
        READ     = "READ",     "已读"
        ARCHIVED = "ARCHIVED", "已归档"

    class Level(models.TextChoices):
        INFO  = "INFO",  "提示"
        WARN  = "WARN",  "警告"
        ERROR = "ERROR", "错误"

    user     = models.ForeignKey(
        'system.User',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="接收用户",
        db_index=True
    )
    type     = models.CharField(max_length=16, choices=Type.choices, verbose_name="消息类型", db_index=True)
    status   = models.CharField(max_length=16, choices=Status.choices, default=Status.UNREAD, verbose_name="状态", db_index=True)
    level    = models.CharField(max_length=8, choices=Level.choices, default=Level.INFO, verbose_name="级别")
    title    = models.CharField(max_length=128, verbose_name="标题", blank=True, default="")
    content  = models.TextField(verbose_name="内容")
    link_url = models.CharField(max_length=256, verbose_name="跳转链接", blank=True, default="")
    extra    = models.JSONField(default=dict, blank=True, verbose_name="附加数据")
    read_at  = models.DateTimeField(null=True, blank=True, verbose_name="阅读时间")

    # 用于去重/幂等（可选）：同一用户+同一 dedup_key 只允许出现一条（例如相同事件重复投递时）
    dedup_key = models.CharField(max_length=128, blank=True, default="", verbose_name="去重键")

    class Meta:
        db_table = "notifications"
        verbose_name = "通知消息"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["user", "status", "-created_at"], name="idx_notice_user_status_ctime"),
            models.Index(fields=["user", "type", "-created_at"], name="idx_notice_user_type_ctime"),
            models.Index(fields=["dedup_key"], name="idx_notice_dedup"),
        ]
        constraints = [
            # dedup_key 非空时，(user, dedup_key) 唯一
            models.UniqueConstraint(
                fields=["user", "dedup_key"],
                condition=~Q(dedup_key=""),
                name="uniq_user_dedup_when_present",
            )
        ]

    def __str__(self):
        return f"[{self.get_type_display()}] {self.title or self.content[:20]}"

class NotificationSetting(BaseModel):
    """
    用户偏好设置：是否接收各类消息、推送通道偏好、免打扰时段等。
    """
    user = models.OneToOneField(
        'system.User',
        on_delete=models.CASCADE,
        related_name='notification_setting',
        verbose_name="用户"
    )

    # 分类开关
    enable_approval = models.BooleanField(default=True, verbose_name="接收审批通知")
    enable_detect   = models.BooleanField(default=True, verbose_name="接收检测通知")
    enable_system   = models.BooleanField(default=True, verbose_name="接收系统通知")

    # 推送通道（根据实际是否做邮件/SMS 再启用）
    channel_websocket = models.BooleanField(default=True, verbose_name="WebSocket推送")
    channel_email     = models.BooleanField(default=False, verbose_name="邮件推送")
    channel_sms       = models.BooleanField(default=False, verbose_name="短信推送")

    # 免打扰（仅影响主动推送，不影响列表查询）
    dnd_start = models.TimeField(null=True, blank=True, verbose_name="免打扰开始")
    dnd_end   = models.TimeField(null=True, blank=True, verbose_name="免打扰结束")

    class Meta:
        db_table = "notification_settings"
        verbose_name = "通知偏好"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user} 的通知偏好"

class NotificationTemplate(BaseModel):
    """
    模板化：系统公告或通用消息可基于模板渲染生成（可选）。
    """
    class Type(models.TextChoices):
        APPROVAL = "APPROVAL", "审批通知"
        DETECT   = "DETECT",   "检测通知"
        SYSTEM   = "SYSTEM",   "系统通知"

    code     = models.CharField(max_length=64, unique=True, verbose_name="模板编码")
    type     = models.CharField(max_length=16, choices=Type.choices, verbose_name="模板类型", db_index=True)
    title    = models.CharField(max_length=128, verbose_name="模板标题")
    content  = models.TextField(verbose_name="模板内容")  # 可使用占位符，如 {{project_name}}、{{approval_id}}
    enabled  = models.BooleanField(default=True, verbose_name="是否启用")

    class Meta:
        db_table = "notification_templates"
        verbose_name = "通知模板"
        verbose_name_plural = verbose_name
        indexes = [models.Index(fields=["type", "enabled"], name="idx_ntpl_type_enabled")]

    def __str__(self):
        return f"{self.code} - {self.title}"

class NotificationOutbox(BaseModel):
    """
    事务外盒（可选）：为“事件→MQ→消费者→入库/推送”链路提供可靠投递。
    业务在事务内写入 outbox，异步 worker 轮询投递，避免跨服务分布式事务问题。
    """
    event_name   = models.CharField(max_length=64, verbose_name="事件名")         # 如 approval.passed / detect.finished
    payload      = models.JSONField(default=dict, blank=True, verbose_name="负载")
    status       = models.CharField(max_length=16, default="PENDING", verbose_name="状态", db_index=True)  # PENDING/SENT/FAILED
    try_count    = models.IntegerField(default=0, verbose_name="重试次数")
    last_error   = models.TextField(blank=True, default="", verbose_name="最后错误")
    next_retry_at= models.DateTimeField(null=True, blank=True, verbose_name="下次重试时间")

    class Meta:
        db_table = "notification_outbox"
        verbose_name = "通知外盒"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["status", "next_retry_at"], name="idx_outbox_status_next"),
            models.Index(fields=["-created_at"], name="idx_outbox_ctime"),
        ]

    def __str__(self):
        return f"{self.event_name}({self.status})"
