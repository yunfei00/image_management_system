from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, TemplateView

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from images.models import BaseImage, BusinessImage
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

class UserDashboardView(LoginRequiredMixin, TemplateView):
    """
    用户主页：显示“创建项目”入口 + “我创建的项目”列表
    """
    template_name = "projects/user_dashboard.html"
    def get(self, request, *args, **kwargs):
        """
        用户主页，展示用户创建的项目、镜像入库记录和基础镜像。
        """
        # 获取当前用户创建的项目
        projects = Project.objects.filter(created_by=request.user).order_by('-submit_at')

        # 获取当前用户上传的镜像（镜像入库）
        # image_repositories = BusinessImage.objects.filter(created_by=request.user).order_by('-created_at')
        image_repositories = BusinessImage.objects.filter().order_by('-created_at')

        # 获取系统中所有的基础镜像
        base_images = BaseImage.objects.all()

        # 渲染模板，传递项目、镜像和基础镜像数据
        return render(request, self.template_name, {
            'projects': projects,
            'image_repositories': image_repositories,
            'base_images': base_images
        })

class ProjectDetailView(LoginRequiredMixin, View):
    template_name = "projects/project_detail.html"

    def get(self, request, pk):
        # 预加载常用外键，保持你项目里的一致写法
        obj = get_object_or_404(
            Project.objects.select_related("department", "applicant", "base_image"),
            pk=pk
        )

        # if not (request.user.is_superuser or obj.created_by_id == request.user.id):
        #     from django.http import HttpResponseForbidden
        #     return HttpResponseForbidden("你无权查看该项目")

        # 简单回跳：优先 ?return=，否则用 Referer，再兜底回列表
        return_url = (
            request.GET.get("return")
            or request.META.get("HTTP_REFERER")
            or str(reverse_lazy("projects:project_list"))
        )

        return render(request, self.template_name, {
            "obj": obj,                 # 与你现有模板/Modal上下文命名保持一致
            "return_url": return_url,
        })

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
            obj = form.save(commit=False)
            obj.created_by = self.request.user
            obj.status = Project.ApprovalStatus.PENDING  # 创建后默认走审批
            obj.save()
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
