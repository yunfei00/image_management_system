from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets

from system.filters_all import DepartmentFilter
from system.forms import DeptForm
from system.models_all import Department
from system.serializers import DepartmentSerializer
from system.utils import export_queryset_to_excel
from system.views_all import render_modal_form


class   DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('-create_time')
    serializer_class = DepartmentSerializer


# ---------- Department ----------
class DeptListView(View):
    def get(self, request):
        f = DepartmentFilter(request.GET, queryset=Department.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)
        if 'export' in request.GET:
            cols = [('id','ID'), ('name','部门名称'), ('status','状态')]
            return export_queryset_to_excel(f.qs, cols, 'departments')
        return render(request, 'system/dept_list.html', {'filter': f, 'page_obj': objs})

class DeptCreateView(View):
    def get(self, request):
        form = DeptForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = DeptForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class DeptUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Department, pk=pk)
        form = DeptForm(instance=obj)
        return render_modal_form(request, form, context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Department, pk=pk)
        form = DeptForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class DeptDeleteView(DeleteView):
    model = Department
    success_url = reverse_lazy('system:dept_list')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})