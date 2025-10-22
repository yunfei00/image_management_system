# projects/filters/project_filter.py
import django_filters
from projects.models import Project
from system.models import Department
from images.models import BaseImage


class ProjectFilter(django_filters.FilterSet):
    # 文本模糊
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains", label="项目名称")
    code = django_filters.CharFilter(field_name="code", lookup_expr="icontains", label="项目编码")
    # 选择型
    department = django_filters.ModelChoiceFilter(queryset=Department.objects.all(), label="部门")
    base_image = django_filters.ModelChoiceFilter(queryset=BaseImage.objects.all(), label="基础镜像")
    status = django_filters.NumberFilter(field_name="status", label="项目状态")
    approval_status = django_filters.NumberFilter(field_name="approval_status", label="审批状态")
    # 时间范围
    plan_online_date = django_filters.DateFromToRangeFilter(field_name="plan_online_date", label="预计上线时间范围")
    submit_at = django_filters.DateTimeFromToRangeFilter(field_name="submit_at", label="提交时间范围")

    class Meta:
        model = Project
        fields = [
            "status", "approval_status", "name", "code", "department",
            "base_image", "plan_online_date", "submit_at"
        ]
