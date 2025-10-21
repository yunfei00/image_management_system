import django_filters

from detection.models import DetectTool


class DetectToolFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    type = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.NumberFilter()

    class Meta:
        model = DetectTool
        fields = ["name", "type", "status"]