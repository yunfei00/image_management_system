from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from system.filters.menu import MenuFilter
from system.forms import MenuForm
from system.models import Menu
from system.serializers.menu import MenuSerializer, MenuTreeSerializer
from system.utils import export_queryset_to_excel
from system.views.handle_modal_form import render_modal_form

# ---------- DRF: 菜单 CRUD ----------
class MenuViewSet(viewsets.ModelViewSet):
    """
    /api/menus CRUD + 过滤 ?name=&status=&parent=&visible=
    """
    queryset = Menu.objects.all().order_by('sort', 'id')
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return MenuFilter(self.request.GET, queryset=qs).qs

# ---------- 用户可见菜单树 ----------
class MyMenuTreeAPIView(APIView):
    """
    GET /api/users/me/menus
    返回当前登录用户可见的启用菜单树（按 sort,id 排序）
    可见规则：
      - 菜单未绑定 groups => 所有已登录用户可见
      - 绑定了 groups => 用户与菜单 groups 有交集才可见
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_groups = set(request.user.groups.values_list('id', flat=True))
        roots = Menu.objects.filter(parent__isnull=True, status=Menu.Status.ENABLED).order_by('sort', 'id')

        def allowed(m: Menu) -> bool:
            g = set(m.groups.values_list('id', flat=True))
            return (not g) or (user_groups & g)

        def build(node: Menu):
            if not allowed(node) or not node.visible:
                return None
            item = {
                'id': node.id, 'name': node.name, 'path': node.path, 'icon': node.icon,
                'sort': node.sort, 'status': node.status, 'visible': node.visible,
                'is_external': node.is_external, 'permission': node.permission, 'children': []
            }
            for child in node.children.filter(status=Menu.Status.ENABLED).order_by('sort', 'id'):
                c = build(child)
                if c:
                    item['children'].append(c)
            return item

        tree = []
        for r in roots:
            x = build(r)
            if x:
                tree.append(x)
        return Response(tree)

# ---------- Web: 列表 / 新增 / 编辑 / 删除 ----------
class MenuListView(View):
    def get(self, request):
        f = MenuFilter(request.GET, queryset=Menu.objects.all())
        qs = f.qs.order_by('sort', 'id')
        print(f'{self.__class__.__name__} request: {request.GET}')
        # 导出：/system/menus/?export=1
        if 'export' in request.GET:
            cols = [
                ('id', 'ID'),
                ('name', '菜单名称'),
                ('path', '路径'),
                ('icon', '图标'),
                ('sort', '排序'),
                ('status', '状态'),
                ('visible', '显示'),
            ]
            return export_queryset_to_excel(qs, cols, 'menus')

        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)

        return render(request, 'system/menu_list.html', {
            'filter': f,
            'page_obj': objs,
        })

class MenuCreateView(View):
    def get(self, request):
        form = MenuForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class MenuUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Menu, pk=pk)
        form = MenuForm(instance=obj)
        return render_modal_form(request, form, context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Menu, pk=pk)
        form = MenuForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class MenuDeleteView(DeleteView):
    model = Menu
    success_url = reverse_lazy('system:menu_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})
