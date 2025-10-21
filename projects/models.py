from django.db import models
from django.utils.translation import gettext_lazy as _  # 正确导入

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="项目名称")
    applicant = models.CharField(max_length=255, verbose_name="申请人")
    department = models.CharField(max_length=100, verbose_name="部门")
    end_user = models.CharField(max_length=255, verbose_name="最终用户")
    description = models.TextField(verbose_name="项目描述")
    plan_online_date = models.DateField(verbose_name="预计上线时间")
    status = models.CharField(max_length=50, verbose_name="项目状态")
    base_image_version = models.CharField(max_length=100, verbose_name="基础镜像版本")
    components = models.JSONField(verbose_name="其他组件")

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目管理"

class ProjectApproval(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目")
    approver = models.CharField(max_length=255, verbose_name="审批人")
    approval_status = models.CharField(max_length=50, verbose_name="审批状态")
    approved_at = models.DateTimeField(auto_now_add=True, verbose_name="审批时间")

    class Meta:
        verbose_name = "项目审批"
        verbose_name_plural = "项目审批管理"


class ApprovalFlow(models.Model):
    class Status(models.IntegerChoices):
        DISABLED = 0, _('禁用')
        ENABLED  = 1, _('启用')

    name = models.CharField(_('流程名称'), max_length=100, unique=True)
    nodes_config = models.JSONField(_('审批节点配置'))  # JSON 结构见下方示例
    status = models.PositiveSmallIntegerField(_('状态'), choices=Status.choices, default=Status.ENABLED)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        db_table = 'approval_flows'
        verbose_name = _('审批流程配置')
        verbose_name_plural = _('审批流程配置')
        indexes = [
            models.Index(fields=['status'], name='idx_flow_status'),
        ]

    def __str__(self):
        return self.name


# [
#   {
#     "id": "n1",
#     "name": "业务负责人审批",
#     "approvers": {"roles": [3], "users": []},
#     "mode": "ANY",          // ANY: 任意一人通过；ALL: 全部通过
#     "timeout_hours": 48,    // 超时自动处理策略可扩展，如 "auto": "pass|reject|notify"
#     "conditions": null      // 可选：按金额/风险等级等触发
#   },
#   {
#     "id": "n2",
#     "name": "安全合规审批",
#     "approvers": {"roles": [5], "users": []},
#     "mode": "ALL",
#     "timeout_hours": 72,
#     "conditions": {"scan_pass": true}
#   }
# ]