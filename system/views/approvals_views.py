# apps/approvals/views.py
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets

from system.filters.approvals_filters import ApprovalFlowFilter
from system.forms import ApprovalFlowForm
from system.models import ApprovalFlow
from system.serializers.approvals_serializers import ApprovalFlowSerializer
from system.utils import export_queryset_to_excel
from system.views.handle_modal_form import render_modal_form


class ApprovalFlowViewSet(viewsets.ModelViewSet):
    """
    /api/approval-flows
    - 列表/详情/新增/更新/删除（DRF）
    - 支持前端通过 ?search= / ?ordering= / filterset 进行过滤与排序（若在 Router/Settings 已开启）
    """
    queryset = ApprovalFlow.objects.all().order_by('-created_at')
    serializer_class = ApprovalFlowSerializer


# ---------- ApprovalFlow Web ----------
class ApprovalFlowListView(View):
    """
    列表 + 搜索 + 导出
    模板: templates/approvals/approval_flow_list.html
    """
    def get(self, request):
        f = ApprovalFlowFilter(request.GET, queryset=ApprovalFlow.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)

        # 导出：与 Department 一致，支持保持当前筛选条件导出
        if 'export' in request.GET:
            cols = [
                ('id', 'ID'),
                ('name', '流程名称'),
                ('status', '状态'),
                ('created_at', '创建时间'),
                # 如需导出节点详情，可加上 nodes_config；Excel 中会以 JSON 字符串形式呈现
                # ('nodes_config', '节点配置'),
            ]
            return export_queryset_to_excel(f.qs, cols, 'approval_flows')

        return render(request, 'system/approval_flow_list.html', {
            'filter': f,
            'page_obj': objs
        })


class ApprovalFlowCreateView(View):
    """
    新增（弹窗表单）
    """
    def get(self, request):
        form = ApprovalFlowForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = ApprovalFlowForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)


class ApprovalFlowUpdateView(View):
    """
    编辑（弹窗表单）
    """
    def get(self, request, pk):
        obj = get_object_or_404(ApprovalFlow, pk=pk)
        form = ApprovalFlowForm(instance=obj)
        return render_modal_form(request, form, context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(ApprovalFlow, pk=pk)
        form = ApprovalFlowForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})


class ApprovalFlowDeleteView(DeleteView):
    """
    删除（与部门视图一致，返回 JSON 以便前端刷新）
    """
    model = ApprovalFlow
    success_url = reverse_lazy('approvals:approval_flow_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})
