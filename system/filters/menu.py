import django_filters
from system.models import Menu

class MenuFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='菜单名称')
    status = django_filters.NumberFilter(field_name='status', label='状态')
    parent = django_filters.NumberFilter(field_name='parent_id', label='父菜单ID')
    visible = django_filters.BooleanFilter(field_name='visible', label='是否显示')

    class Meta:
        model = Menu
        fields = ['status', 'name', 'parent', 'visible', 'is_external']
