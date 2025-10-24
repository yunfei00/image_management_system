import django_filters

from detection.models import SecurityDetectApply


class SecurityDetectApplyFilter(django_filters.FilterSet):
    project_name = django_filters.CharFilter(field_name='project__name', lookup_expr='icontains', label='项目名称')
    status = django_filters.ChoiceFilter(choices=SecurityDetectApply.STATUS_CHOICES, label='检测状态')

    class Meta:
        model = SecurityDetectApply
        fields = ['status', 'project_name']
