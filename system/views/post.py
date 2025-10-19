from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets

from system.filters.post_filter import PositionFilter
from system.forms import PositionForm
from system.models import Position
from system.serializers.post import PositionSerializer
from system.utils import export_queryset_to_excel
from system.views.handle_modal_form import render_modal_form

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all().order_by('-created_at')
    serializer_class = PositionSerializer

# ---------- Position ----------
class PostListView(View):
    def get(self, request):
        f = PositionFilter(request.GET, queryset=Position.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)
        if 'export' in request.GET:
            cols = [('id','ID'), ('name','岗位名称'), ('status','状态')]
            return export_queryset_to_excel(f.qs, cols, 'position')
        return render(request, 'system/post_list.html', {'filter': f, 'page_obj': objs})


class PostCreateView(View):
    def get(self, request):
        form = PositionForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class PostUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Position, pk=pk)
        form = PositionForm(instance=obj)
        return render_modal_form(request, form, context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Position, pk=pk)
        form = PositionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class PostDeleteView(DeleteView):
    model = Position
    success_url = reverse_lazy('system:post_list')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})