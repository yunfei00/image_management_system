# notifications/filters/notification_filter.py
import django_filters

from notification.models import Notification


class NotificationFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type', lookup_expr='exact', label='消息类型')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact', label='状态')
    start = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte', label='开始时间')
    end = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte', label='结束时间')

    class Meta:
        model = Notification
        fields = ['type', 'status']
