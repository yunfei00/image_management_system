import django_filters

from detection.models import ProjectDetectTool


class ProjectDetectToolFilter(django_filters.FilterSet):
    project   = django_filters.NumberFilter(field_name="project_id", label="项目ID")
    tool      = django_filters.NumberFilter(field_name="tool_id", label="工具ID")
    available = django_filters.NumberFilter(field_name="available", label="可用性")
    tool_type = django_filters.CharFilter(field_name="tool__type", lookup_expr="exact", label="工具类型")
    tool_name = django_filters.CharFilter(field_name="tool__name", lookup_expr="icontains", label="工具名称")

    class Meta:
        model = ProjectDetectTool
        fields = ["project", "tool", "available", "tool_type", "tool_name"]
