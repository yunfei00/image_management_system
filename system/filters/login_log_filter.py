# system/filters/login_log_filter.py
import django_filters
from system.models.log_manager import LoginLog


class LoginLogFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(field_name='login_time', lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name='login_time', lookup_expr='lte')
    username = django_filters.CharFilter(lookup_expr='icontains')
    ip = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = LoginLog
        fields = ['username', 'ip', 'status', 'start_time', 'end_time']
