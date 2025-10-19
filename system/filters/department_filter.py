import django_filters
from system.models import Department

class DepartmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='部门名称')

    class Meta:
        model = Department
        fields = ['status', 'name']