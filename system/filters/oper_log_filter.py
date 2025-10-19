import django_filters
from system.models import OperationLog


class OperationLogFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(field_name='operation_time', lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name='operation_time', lookup_expr='lte')
    module = django_filters.CharFilter(lookup_expr='icontains')
    operator = django_filters.CharFilter(lookup_expr='icontains')
    ip = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = OperationLog
        fields = ['start_time', 'end_time', 'module', 'operator', 'ip']
