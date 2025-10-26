# images/views.py
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets

from projects.models import Project
from .filters import BaseImageFilter, BusinessImageFilter
from .forms import BaseImageForm, BusinessImageForm
from .models import BaseImage, BusinessImage
from .serializers import BaseImageSerializer, BusinessImageSerializer

# 复用你项目里的工具（与 Department 一致）
from system.utils import export_queryset_to_excel, print_objs
from system.views.handle_modal_form import render_modal_form


# ---------- API ----------
class BaseImageViewSet(viewsets.ModelViewSet):
    queryset = BaseImage.objects.all().order_by('-created_at')
    serializer_class = BaseImageSerializer

class BusinessImageViewSet(viewsets.ModelViewSet):
    queryset = BusinessImage.objects.select_related('project').all().order_by('-created_at')
    serializer_class = BusinessImageSerializer


# ---------- BaseImage ----------
class BaseImageListView(View):
    def get(self, request):
        print(f'{self.__class__.__name__} get is {request.GET}')
        f = BaseImageFilter(request.GET, queryset=BaseImage.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)
        print_objs(objs)
        if 'export' in request.GET:
            cols = [
                ('id', 'ID'), ('name', '镜像名称'), ('version', '版本'),
                ('image_id', '镜像ID'), ('status', '状态'), ('category', '分类'),
                ('size', '大小'), ('created_at', '创建时间'),
            ]
            return export_queryset_to_excel(f.qs, cols, 'base_images')
        return render(request, 'images/base_image_list.html', {'filter': f, 'page_obj': objs})

class BaseImageCreateView(View):
    def get(self, request):
        form = BaseImageForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = BaseImageForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class BaseImageUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(BaseImage, pk=pk)
        form = BaseImageForm(instance=obj)
        return render_modal_form(request, form, context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(BaseImage, pk=pk)
        form = BaseImageForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class BaseImageDeleteView(DeleteView):
    model = BaseImage
    success_url = reverse_lazy('images:base_list')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})


# ---------- BusinessImage ----------
class BusinessImageListView(View):
    def get(self, request):
        f = BusinessImageFilter(
            request.GET,
            queryset=BusinessImage.objects.select_related('project').all()
        )
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)
        if 'export' in request.GET:
            cols = [
                ('id', 'ID'), ('name', '镜像名称'), ('version', '版本'),
                ('image_id', '镜像ID'), ('project', '项目'),
                ('detect_status', '检测状态'), ('approve_status', '审批状态'),
                ('size', '大小'), ('created_at', '创建时间'),
            ]
            return export_queryset_to_excel(f.qs, cols, 'business_images')
        return render(request, 'images/business_image_list.html', {'filter': f, 'page_obj': objs})

class BusinessImageCreateView(View):
    def get(self, request):
        form = BusinessImageForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = BusinessImageForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class BusinessImageUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(BusinessImage, pk=pk)
        form = BusinessImageForm(instance=obj)
        return render_modal_form(request, form, context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(BusinessImage, pk=pk)
        form = BusinessImageForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class BusinessImageDeleteView(DeleteView):
    model = BusinessImage
    success_url = reverse_lazy('images:biz_list')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})


def upload_business_image(request):
    if request.method == 'POST' and request.FILES['image']:
        print(f'upload_business_image receve post data is {request.POST}')
        # 获取表单数据
        image_file = request.FILES['image']
        image_name = request.POST['name']
        image_version = request.POST['version']
        project_id = request.POST['project']

        # 获取所属项目
        project = Project.objects.get(id=project_id)

        # 保存文件
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        file_url = fs.url(filename)

        # 获取文件大小（以MB为单位）
        file_size = image_file.size / (1024 * 1024)  # 转换为MB

        # 保存镜像数据到数据库
        business_image = BusinessImage.objects.create(
            name=image_name,
            version=image_version,
            project=project,
            image_id=filename,  # 也可以使用文件名作为镜像ID
            size=file_size,
            image_file=filename  # 保存上传的镜像文件路径
        )

        # 上传后重定向到用户主页，显示镜像
        return redirect('projects:user_dashboard')  # 假设用户主页的URL名是'user_dashboard'

    # 获取所有项目列表，用于显示在表单中
    projects = Project.objects.all()
    return render(request, 'projects/user_dashboard.html', {'projects': projects})