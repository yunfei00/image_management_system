import django_filters
from system.models.post import Position

class PositionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    code = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.NumberFilter()

    class Meta:
        model = Position
        fields = ["name", "code", "status"]