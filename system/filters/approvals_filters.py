import django_filters
from system.models import ApprovalFlow

class ApprovalFlowFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains", label="名称")
    status = django_filters.NumberFilter(field_name="status", label="状态")

    class Meta:
        model = ApprovalFlow
        fields = ["name", "status"]
