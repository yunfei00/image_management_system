import django_filters

from detection.models import DetectTool


class DetectToolFilter(django_filters.FilterSet):
    name  = django_filters.CharFilter(field_name="name", lookup_expr="icontains", label="工具名称")
    type  = django_filters.CharFilter(field_name="type", lookup_expr="exact", label="工具类型")
    status = django_filters.NumberFilter(field_name="status", lookup_expr="exact", label="状态")

    class Meta:
        model = DetectTool
        fields = ["status", "type", "name"]
