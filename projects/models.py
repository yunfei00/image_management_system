from django.db import models

# Create your models here.
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    class Status(models.IntegerChoices):
        DISABLED = 0, _("禁用")
        ENABLED  = 1, _("启用")

    class ApprovalStatus(models.IntegerChoices):
        PENDING  = 0, _("待审批")
        APPROVED = 1, _("已通过")
        REJECTED = 2, _("已拒绝")

    code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="项目编码")
    name = models.CharField(max_length=255, verbose_name="项目名称")

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="applied_projects", verbose_name="申请人"
    )
    department = models.ForeignKey(
        "system.Department", on_delete=models.PROTECT,
        verbose_name="部门"
    )

    end_user = models.CharField(max_length=255, verbose_name="最终用户")
    description = models.TextField(blank=True, verbose_name="项目描述")
    plan_online_date = models.DateField(null=True, blank=True, verbose_name="预计上线时间")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="创建人",
        on_delete=models.PROTECT,
        related_name="created_projects",
        editable=False,                 # ★ 前台/接口不可编辑，必须后端写入当前用户
        db_index=True,                  # ★ “我的项目”查询性能更好
        blank=True,
        null=True,
    )

    # 基础镜像（禁止被误删）
    base_image = models.ForeignKey(
        "images.BaseImage", on_delete=models.PROTECT,
        related_name="projects", verbose_name="基础镜像"
    )

    components = models.JSONField(default=list, blank=True, verbose_name="其他组件")

    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.ENABLED, verbose_name="项目状态"
    )
    approval_status = models.PositiveSmallIntegerField(
        choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING, verbose_name="审批状态"
    )

    # ★ 审批对接的补充字段（便于统计与审计）
    approval_required = models.BooleanField("是否需要审批", default=True, db_index=True)  # 某些小项目可跳过
    approved_at = models.DateTimeField("审批通过时间", null=True, blank=True)             # 审批通过时写入
    rejected_at = models.DateTimeField("审批拒绝时间", null=True, blank=True)            # 审批拒绝时写入

    # ★ 归档（软删除/隐藏）能力，避免物理删除
    is_archived = models.BooleanField("是否归档", default=False, db_index=True)
    archived_at = models.DateTimeField("归档时间", null=True, blank=True)

    submit_at = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目管理"
        ordering = ["-submit_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["approval_status"]),
            models.Index(fields=["department", "status"]),
            models.Index(fields=["base_image", "status"]),
            models.Index(fields=["created_by", "status", "approval_status"]),  # ★ “我的项目”+状态页常用组合
            models.Index(fields=["submit_at"]),                                 # ★ 与默认排序配合
            models.Index(fields=["is_archived"]),                               # ★ 归档筛选
        ]
        constraints = [
            models.UniqueConstraint(fields=["name", "department"], name="uniq_project_name_in_department"),
            # ★ 若使用 PostgreSQL，建议改为大小写不敏感唯一（替换上面的 code=unique=True）：
            # models.UniqueConstraint(Lower("code"), name="uniq_project_code_ci"),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def base_image_version(self) -> str:
        return getattr(self.base_image, "version", "")

    # ★ 可选：便捷判断
    @property
    def need_approval(self) -> bool:
        return self.approval_required and self.approval_status == self.ApprovalStatus.PENDING


class ProjectMember(models.Model):
    class Role(models.TextChoices):
        OWNER   = "owner", "项目管理员"
        DEV     = "dev", "承建方人员"
        OPS     = "ops", "运维"
        AUDITOR = "auditor", "审计"

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="members", verbose_name="项目"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_memberships", verbose_name="用户"
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DEV, verbose_name="项目内角色")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")

    class Meta:
        verbose_name = "项目成员"
        verbose_name_plural = "项目成员"
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.project.code}:{self.user}({self.role})"



# class ProjectApproval(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="项目")
#     approver = models.CharField(max_length=255, verbose_name="审批人")
#     approval_status = models.CharField(max_length=50, verbose_name="审批状态")
#     approved_at = models.DateTimeField(auto_now_add=True, verbose_name="审批时间")
#
#     class Meta:
#         verbose_name = "项目审批"
#         verbose_name_plural = "项目审批管理"


# class ApprovalFlow(models.Model):
#     class Status(models.IntegerChoices):
#         DISABLED = 0, '禁用'
#         ENABLED  = 1, '启用'
#
#     name = models.CharField('流程名称', max_length=100, unique=True)
#     nodes_config = models.JSONField('审批节点配置')  # JSON 结构见下方示例
#     status = models.PositiveSmallIntegerField('状态', choices=Status.choices, default=Status.ENABLED)
#     created_at = models.DateTimeField('创建时间', auto_now_add=True)
#     updated_at = models.DateTimeField('更新时间', auto_now=True)
#
#     class Meta:
#         db_table = 'approval_flows'
#         verbose_name = '审批流程配置'
#         verbose_name_plural = '审批流程配置'
#         indexes = [
#             models.Index(fields=['status'], name='idx_flow_status'),
#         ]
#
#     def __str__(self):
#         return self.name


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