from django.http import HttpResponse
from django.views.generic import ListView
from django.utils import timezone
import csv
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ..filters.oper_log_filter import OperationLogFilter
from ..forms import OperationLogSearchForm
from ..models import OperationLog
from ..serializers.oper_log_serializer import OperationLogSerializer


# ---- DRF ViewSet ----
class OperationLogViewSet(viewsets.ModelViewSet):
    """
    API: /api/logs/operation/
    支持：list, retrieve, destroy（单个），
    额外 action：bulk_delete (POST), export_csv (GET)
    """
    queryset = OperationLog.objects.all().order_by('-operation_time')
    serializer_class = OperationLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OperationLogFilter
    search_fields = ['module', 'operator', 'ip', 'operation_content']
    ordering_fields = ['operation_time', 'module', 'operator']

    # 批量删除
    @action(detail=False, methods=['post'], url_path='bulk_delete')
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        if not isinstance(ids, list):
            return Response({"detail": "ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)
        qs = OperationLog.objects.filter(id__in=ids)
        count = qs.count()
        qs.delete()
        return Response({"deleted": count})

    # 导出 CSV（根据当前 filter）
    @action(detail=False, methods=['get'], url_path='export_csv')
    def export_csv(self, request):
        # 使用 filter 后的 queryset
        qs = self.filter_queryset(self.get_queryset())

        # 创建 CSV 响应
        response = HttpResponse(content_type='text/csv')
        filename = f"operation_logs_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(['id', 'operation_time', 'module', 'operator', 'ip', 'operation_content'])
        for obj in qs:
            writer.writerow([
                obj.id,
                obj.operation_time.isoformat(),
                obj.module,
                obj.operator,
                obj.ip or '',
                obj.operation_content.replace('\n', ' ')[:10000]  # 避免换行破坏 csv
            ])
        return response

# ---- 用户 API: 当前登录用户的日志 ----
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class UserOperationLogsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        qs = OperationLog.objects.filter(operator=username).order_by('-operation_time')[:100]  # 限制数量
        serializer = OperationLogSerializer(qs, many=True)
        return Response(serializer.data)

class OperationLogListView(ListView):
    model = OperationLog
    template_name = "system/operation_log_list.html"
    context_object_name = "logs"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().order_by('-operation_time')
        form = OperationLogSearchForm(self.request.GET)
        if form.is_valid():
            module = form.cleaned_data.get('module')
            operator = form.cleaned_data.get('operator')
            ip = form.cleaned_data.get('ip')
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            if module:
                qs = qs.filter(module__icontains=module)
            if operator:
                qs = qs.filter(operator__icontains=operator)
            if ip:
                qs = qs.filter(ip__icontains=ip)
            if start_time:
                qs = qs.filter(operation_time__gte=start_time)
            if end_time:
                qs = qs.filter(operation_time__lte=end_time)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = OperationLogSearchForm(self.request.GET)
        return ctx
