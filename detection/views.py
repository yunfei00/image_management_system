from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from detection.filters.detect_tool_filter import DetectToolFilter
from detection.filters.pre_detect_record_filter import PreDetectRecordFilter
from detection.filters.project_detect_tool_filter import ProjectDetectToolFilter
from detection.forms import PreDetectRecordForm, DetectToolForm, ProjectDetectToolForm
from detection.models import DetectTool, ProjectDetectTool, PreDetectRecord
from detection.serializers.detect_tool import DetectToolSerializer
from detection.serializers.pre_detect_record import PreDetectSerializer, PreDetectCreateSerializer
from detection.serializers.project_detect_tool import ProjectDetectToolSerializer
# 你现有的工具函数/表单（与部门模块一致）
from system.utils import export_queryset_to_excel
from system.views.handle_modal_form import render_modal_form

# ====== API (DRF) ======
class DetectToolViewSet(viewsets.ModelViewSet):
    queryset = DetectTool.objects.all().order_by("-created_at")
    serializer_class = DetectToolSerializer

class ProjectDetectToolViewSet(viewsets.ModelViewSet):
    queryset = ProjectDetectTool.objects.select_related("project","tool").all().order_by("-id")
    serializer_class = ProjectDetectToolSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # 支持 ?project=<id> 快速筛
        project_id = self.request.query_params.get("project")
        return qs.filter(project_id=project_id) if project_id else qs

    @action(methods=["post"], detail=False, url_path="test")
    def test_all(self, request):
        """Demo: 批量测试把可用性置为 OK，可传 ids 指定行"""
        ids = request.data.get("ids")
        qs = self.get_queryset()
        if ids: qs = qs.filter(id__in=ids)
        updated = qs.update(available=ProjectDetectTool.Availability.OK)
        return Response({"updated": updated})

class PreDetectViewSet(viewsets.ModelViewSet):
    queryset = PreDetectRecord.objects.select_related("project","tool").all().order_by("-id")
    serializer_class = PreDetectSerializer

    def create(self, request, *args, **kwargs):
        ser = PreDetectCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        rec = ser.save(status=PreDetectRecord.Status.PENDING)
        # Demo：秒回成功（后续你可接 Celery 异步）
        now = timezone.now()
        rec.started_at = now
        rec.detect_time = now
        rec.status = PreDetectRecord.Status.SUCCESS
        rec.report_path = f"reports/{rec.id}.pdf"
        rec.vulnerability_count = 3
        rec.save(update_fields=["started_at","detect_time","status","report_path","vulnerability_count"])
        return Response(PreDetectSerializer(rec).data, status=201)

    @action(methods=["get"], detail=True, url_path="report")
    def download_report(self, request, pk=None):
        rec = self.get_object()
        # Demo：返回报告路径（真实项目可走签名URL/反向代理）
        return Response({"report_path": rec.report_path})

# ====== Web (List/Create/Update/Delete) ======
# ---- DetectTool ----
class DetectToolListView(View):
    template_name = "detects/tool_list.html"
    def get(self, request):
        f = DetectToolFilter(request.GET, queryset=DetectTool.objects.all())
        qs = f.qs.order_by("-id")
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get("page"))
        if "export" in request.GET:
            cols = [("id","ID"),("name","工具名称"),("type","工具类型"),("status","状态")]
            return export_queryset_to_excel(f.qs, cols, "detect_tools")
        return render(request, self.template_name, {"filter": f, "page_obj": objs})

class DetectToolCreateView(View):
    def get(self, request):
        form = DetectToolForm()
        return render_modal_form(request, form)
    def post(self, request):
        form = DetectToolForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return render_modal_form(request, form)

class DetectToolUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(DetectTool, pk=pk)
        form = DetectToolForm(instance=obj)
        return render_modal_form(request, form, context_extra={"obj": obj})
    def post(self, request, pk):
        obj = get_object_or_404(DetectTool, pk=pk)
        form = DetectToolForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return render_modal_form(request, form, context_extra={"obj": obj})

class DetectToolDeleteView(DeleteView):
    model = DetectTool
    success_url = reverse_lazy("detects:tool_list")
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})

# ---- ProjectDetectTool ----
class ProjectDetectToolListView(View):
    template_name = "detection/project_tool_list.html"
    def get(self, request):
        f = ProjectDetectToolFilter(request.GET, queryset=ProjectDetectTool.objects.select_related("project","tool"))
        qs = f.qs.order_by("-id")
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get("page"))
        if "export" in request.GET:
            cols = [("id","ID"),("project","项目"),("tool","检测工具"),("available","可用性")]
            return export_queryset_to_excel(f.qs, cols, "project_detect_tools")
        return render(request, self.template_name, {"filter": f, "page_obj": objs})

class ProjectDetectToolCreateView(View):
    def get(self, request):
        form = ProjectDetectToolForm()
        return render_modal_form(request, form)
    def post(self, request):
        form = ProjectDetectToolForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return render_modal_form(request, form)

class ProjectDetectToolUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(ProjectDetectTool, pk=pk)
        form = ProjectDetectToolForm(instance=obj)
        return render_modal_form(request, form, context_extra={"obj": obj})
    def post(self, request, pk):
        obj = get_object_or_404(ProjectDetectTool, pk=pk)
        form = ProjectDetectToolForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return render_modal_form(request, form, context_extra={"obj": obj})

class ProjectDetectToolDeleteView(DeleteView):
    model = ProjectDetectTool
    success_url = reverse_lazy("detects:project_tool_list")
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})

# ---- PreDetectRecord ----
class PreDetectListView(View):
    template_name = "detection/pre_detect_list.html"
    def get(self, request):
        f = PreDetectRecordFilter(request.GET, queryset=PreDetectRecord.objects.select_related("project","tool"))
        qs = f.qs.order_by("-id")
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get("page"))
        if "export" in request.GET:
            cols = [
                ("id","ID"),("project","业务方名称"),("tool","检测项"),
                ("detect_time","检测时间"),("status","状态"),("vulnerability_count","漏洞数量")
            ]
            return export_queryset_to_excel(f.qs, cols, "pre_detect_records")

        status_choices = PreDetectRecord.Status.choices
        return render(request, self.template_name, {"filter": f, "page_obj": objs,
                                                    "status_choices": status_choices})

class PreDetectCreateView(View):
    def get(self, request):
        form = PreDetectRecordForm()
        return render_modal_form(request, form)
    def post(self, request):
        form = PreDetectRecordForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"success": True, "id": obj.id})
        return render_modal_form(request, form)

class PreDetectUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(PreDetectRecord, pk=pk)
        form = PreDetectRecordForm(instance=obj)
        return render_modal_form(request, form, context_extra={"obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(PreDetectRecord, pk=pk)
        form = PreDetectRecordForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return render_modal_form(request, form, context_extra={"obj": obj})

class PreDetectDeleteView(DeleteView):
    model = PreDetectRecord
    success_url = reverse_lazy("detects:pre_detect_list")
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})
