from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets

from system.filters import DetectToolFilter
from system.forms import ToolForm
from system.models import DetectTool
from system.serializers.detect_tool import DetectToolSerializer
from system.utils import export_queryset_to_excel
from system.views.handle_modal_form import render_modal_form

class ToolViewSet(viewsets.ModelViewSet):
    queryset = DetectTool.objects.all().order_by('-created_at')
    serializer_class = DetectToolSerializer

# ---------- Detect Tool ----------
class ToolListView(View):
    def get(self, request):
        f = DetectToolFilter(request.GET, queryset=DetectTool.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)
        if 'export' in request.GET:
            cols = [('id','ID'), ('name','工具名称'), ('type','类型'), ('api_url','API地址'),
                    ('config','配置参数'), ('last_test_time','最后测试时间'), ('status','状态')]
            return export_queryset_to_excel(f.qs, cols, 'detect_tool')
        return render(request, 'system/tool_list.html', {'filter': f, 'page_obj': objs})


class ToolCreateView(View):
    def get(self, request):
        form = ToolForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = ToolForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class ToolUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(DetectTool, pk=pk)
        form = ToolForm(instance=obj)
        return render_modal_form(request, form, context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(DetectTool, pk=pk)
        form = ToolForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class ToolDeleteView(DeleteView):
    model = DetectTool
    success_url = reverse_lazy('system:tool_list')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})