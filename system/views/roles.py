from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets

from system.filters_all import RoleFilter
from system.forms import  RoleForm
from system.models_all import  Role
from system.serializers import RoleSerializer
from system.utils import export_queryset_to_excel
from system.views_all import render_modal_form


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# ---------- Role ----------
class RoleListView(View):
    def get(self, request):
        f = RoleFilter(request.GET, queryset=Role.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        if 'export' in request.GET:
            cols = [('id','ID'), ('name','角色名称'), ('code','权限标识'), ('status','状态')]
            return export_queryset_to_excel(f.qs, cols, 'roles')
        return render(request, 'system/role_list.html', {'filter': f, 'page_obj': objs})

class RoleCreateView(View):
    def get(self, request):
        return render_modal_form(request, RoleForm())

    def post(self, request):
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class RoleUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Role, pk=pk)
        return render_modal_form(request, RoleForm(instance=obj), context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Role, pk=pk)
        form = RoleForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class RoleDeleteView(DeleteView):
    model = Role
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})