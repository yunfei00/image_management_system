import django_filters

from report.models import Report


class ReportFilter(django_filters.FilterSet):
    # 按报表类型筛选
    type = django_filters.ChoiceFilter(choices=Report.ReportType.choices, label='报表类型')

    # 按时间段筛选
    period = django_filters.CharFilter(field_name='period', lookup_expr='icontains', label='时间段')

    # 按项目状态筛选（如果有）
    project_status = django_filters.CharFilter(field_name='project_status', lookup_expr='icontains', label='项目状态')

    # 按部门筛选（如果有）
    department = django_filters.CharFilter(field_name='department', lookup_expr='icontains', label='部门')

    class Meta:
        model = Report
        fields = ['type', 'period', 'project_status', 'department']
