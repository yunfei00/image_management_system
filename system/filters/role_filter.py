import django_filters
from system.models.role import Role

class RoleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    code = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.NumberFilter()

    class Meta:
        model = Role
        fields = ["name", "code", "status"]