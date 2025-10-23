import django_filters

from detection.models import PreDetectRecord


class PreDetectRecordFilter(django_filters.FilterSet):
    project = django_filters.NumberFilter(field_name="project_id", label="项目ID")
    tool    = django_filters.NumberFilter(field_name="tool_id", label="工具ID")
    status  = django_filters.CharFilter(field_name="status", lookup_expr="exact", label="状态")
    request_id = django_filters.CharFilter(field_name="request_id", lookup_expr="icontains", label="请求ID")
    detect_time = django_filters.DateFromToRangeFilter(field_name="detect_time", label="检测时间范围")

    class Meta:
        model = PreDetectRecord
        fields = ["project", "tool", "status", "request_id", "detect_time"]
