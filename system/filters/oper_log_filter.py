import django_filters
from system.models import OperationLog


class LoginLogFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(field_name='operation_time', lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name='operation_time', lookup_expr='lte')
    username = django_filters.CharFilter(lookup_expr='icontains')
    ip = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = OperationLog
        fields = {
            'module': ['exact', 'icontains'],
            'operator': ['exact', 'icontains'],
            'ip': ['exact', 'icontains'],
        }
