# images/views.py
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets

from .filters import BaseImageFilter, BusinessImageFilter
from .forms import BaseImageForm, BusinessImageForm
from .models import BaseImage, BusinessImage
from .serializers import BaseImageSerializer, BusinessImageSerializer

# 复用你项目里的工具（与 Department 一致）
from system.utils import export_queryset_to_excel
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
        f = BaseImageFilter(request.GET, queryset=BaseImage.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)
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
