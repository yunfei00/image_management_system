from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from projects.filters import ProjectFilter
from projects.models import Project
from projects.serializers import ProjectSerializer

# 如同部门模块，沿用你现有的工具与表单
from system.utils import export_queryset_to_excel
from system.views.handle_modal_form import render_modal_form
from projects.forms import ProjectForm  # 确保已存在 ModelForm


# ------ DRF ------
class ProjectViewSet(viewsets.ModelViewSet):
    # queryset = Project.objects.select_related("applicant", "department", "base_image", "approval_flow") \
    #                           .all().order_by("-submit_at")
    queryset = Project.objects.select_related("applicant", "department", "base_image",) \
                              .all().order_by("-submit_at")
    serializer_class = ProjectSerializer

    # 企业级常用：鉴权 + 过滤 + 搜索 + 排序
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ["name", "code", "description", "end_user"]
    ordering_fields = ["submit_at", "updated_at", "plan_online_date", "name", "code"]
    ordering = ["-submit_at"]


# ------ Web ------
class ProjectListView(View):
    template_name = "projects/project_list.html"

    def get(self, request):
        f = ProjectFilter(request.GET, queryset=Project.objects.select_related(
            "department", "applicant", "base_image").all())
        qs = f.qs.order_by("-id")
        paginator = Paginator(qs, 10)
        page = request.GET.get("page")
        objs = paginator.get_page(page)

        # 导出
        if "export" in request.GET:
            # 简洁起见，导出原始字段（与部门一致导出 status 数值；也可扩展为 *_display）
            cols = [
                ("id", "ID"),
                ("code", "项目编码"),
                ("name", "项目名称"),
                ("department", "部门"),
                ("applicant", "申请人"),
                ("status", "项目状态"),
                ("approval_status", "审批状态"),
                ("base_image", "基础镜像"),
                ("plan_online_date", "预计上线"),
                ("submit_at", "提交时间"),
            ]
            return export_queryset_to_excel(f.qs, cols, "projects")

        return render(request, self.template_name, {"filter": f, "page_obj": objs})


class ProjectCreateView(View):
    def get(self, request):
        form = ProjectForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return render_modal_form(request, form)


class ProjectUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Project, pk=pk)
        form = ProjectForm(instance=obj)
        return render_modal_form(request, form, context_extra={"obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(Project, pk=pk)
        form = ProjectForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        return render_modal_form(request, form, context_extra={"obj": obj})


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("projects:project_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})
