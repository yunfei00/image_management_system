# images/views.py
from decimal import Decimal, ROUND_HALF_UP

from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
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


# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .tasks import push_image_to_registry


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
        form = BaseImageForm(request.POST, request.FILES)
        if not form.is_valid():
            return render_modal_form(request, form)

        # 不再手动用 FileSystemStorage 保存！让 ModelForm/Model 自己保存文件。
        image_file = request.FILES.get('image_file')

        instance = form.save(commit=False)

        # —— 计算并写入 size（以 MB 存，两位小数）——
        # if image_file:
        #     size_mb = (Decimal(image_file.size) / Decimal(1024 * 1024)).quantize(
        #         Decimal('0.01'), rounding=ROUND_HALF_UP
        #     )
        #     instance.size = size_mb
        if image_file:
            instance.size = image_file.size  # 直接字节数
        # 如果你的表单里没包含一些只读/自动字段（比如 image_id），可以在这里顺手补：
        # instance.image_id = instance.image_id or gen_image_id(...)  # 视情况

        instance.save()    # 这一步会把文件保存到 FileField 的 upload_to 指定目录
        return JsonResponse({'success': True})

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
        form = BusinessImageForm(request.POST, request.FILES)
        if not form.is_valid():
            return render_modal_form(request, form)

        image_file = request.FILES.get('image_file')
        if not image_file:
            # 没有文件直接返回表单（前端会显示必填校验）
            return render_modal_form(request, form)

        # 先构造实例，补充派生字段
        instance = form.save(commit=False)

        # 注意：此时 instance.project 已由表单校验后的数据填入（如果表单包含 project 字段）
        # 若你的表单不包含 project 字段，可手动取 request.POST 再赋值：
        # instance.project = get_object_or_404(Project, id=request.POST.get('project'))

        instance.size = image_file.size  # 字节数
        # 使用原始文件名作为 image_id 或者自定义生成算法
        instance.image_id = instance.image_id or image_file.name

        # 很关键：把上传的文件对象赋给 FileField，后续 save() 会按 upload_to=business/... 保存到 MEDIA_ROOT 下
        instance.image_file = image_file

        instance.save()  # 这一步会真正把文件保存到 business/ 子目录
        return JsonResponse({'success': True})

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
    print(f'request files is {request.FILES}')
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


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image_file'):
        image_file = request.FILES['image_file']
        project_slug = 'your_project_slug'  # 替换为实际项目标识
        app_name = 'hello'  # 替换为实际镜像名
        tag = 'dev'  # 替换为实际标签

        # 保存文件到本地
        image_zip_path = f'/data/app/media/{project_slug}/uploads/{image_file.name}'
        with open(image_zip_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # 调用 Celery 任务进行上传与推送
        push_image_to_registry.delay(image_zip_path, project_slug, app_name, tag)

        return JsonResponse({'status': 'success', 'message': 'Image uploaded and pushed to registry.'})

    return JsonResponse({'status': 'error', 'message': 'No file uploaded.'})


def base_image_download(request, image_id):
    # Retrieve the BaseImage object based on the image_id
    image = get_object_or_404(BaseImage, id=image_id)

    # Get the file path of the image using the get_image_file_path method
    file_path = image.get_image_file_path()

    # Get the original file name (this includes the file extension)
    file_name = image.image_file.name.split('/')[-1]  # Extract the actual file name from the path

    # Open the image file and send it as an HTTP response for download
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'  # Use the original filename
        return response


def base_image_details(request, image_id):
    image = get_object_or_404(BaseImage, id=image_id)
    return render(request, 'images/base_image_details.html', {'image': image})


def business_image_download(request, image_id):
    # Retrieve the BaseImage object based on the image_id
    image = get_object_or_404(BusinessImage, id=image_id)

    # Get the file path of the image using the get_image_file_path method
    file_path = image.get_image_file_path()

    # Get the original file name (this includes the file extension)
    file_name = image.image_file.name.split('/')[-1]  # Extract the actual file name from the path

    # Open the image file and send it as an HTTP response for download
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'  # Use the original filename
        return response


def business_image_details(request, image_id):
    image = get_object_or_404(BusinessImage, id=image_id)
    return render(request, 'images/business_image_details.html', {'image': image})
