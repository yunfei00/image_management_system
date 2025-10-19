import django_filters
from system.models.user import User


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['status', 'name', 'phone']
