from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView

# Create your views here.
from rest_framework import viewsets

from system.utils import export_queryset_to_excel
from .filters.report_filter import ReportFilter
from .models import Report
from django.shortcuts import get_object_or_404, render
from .forms import ReportForm
from .models import Report

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Report
from .serializers.report_serializer import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer


class ReportListView(View):
    def get(self, request):
        # 创建过滤器实例
        f = ReportFilter(request.GET, queryset=Report.objects.all())
        qs = f.qs.order_by('-created_at')

        # 分页
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)

        # 导出功能
        if 'export' in request.GET:
            cols = [('id', 'ID'), ('type', '报表类型'), ('created_at', '创建时间'), ('period', '时间段')]
            return export_queryset_to_excel(f.qs, cols, 'reports')

        # 渲染报表列表模板
        return render(request, 'system/report_list.html', {'filter': f, 'page_obj': objs})


class ReportDeleteView(DeleteView):
    model = Report
    success_url = reverse_lazy('system:report-list')  # 删除后跳转到报表列表页面

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})  # 返回成功删除的消息


class ReportUpdateView(View):
    def get(self, request, pk):
        # 获取要编辑的报表对象
        report = get_object_or_404(Report, pk=pk)
        form = ReportForm(instance=report)
        return render(request, 'system/report_update.html', {'form': form, 'report': report})

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()  # 保存更新的数据
            return JsonResponse({'success': True})  # 返回成功更新的消息
        return render(request, 'system/report_update.html', {'form': form, 'report': report})
