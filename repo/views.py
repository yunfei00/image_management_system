from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets

from repo.filters import RepositoryFilter
from repo.forms import RepositoryForm
from repo.models import Repository
from repo.serializers import RepositorySerializer
from system.utils import export_queryset_to_excel
from system.views.handle_modal_form import render_modal_form

# ---------- Repository ViewSet (for API) ----------
class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all().order_by('-created_at')
    serializer_class = RepositorySerializer

# ---------- Repository List View ----------
class RepositoryListView(View):
    def get(self, request):
        f = RepositoryFilter(request.GET, queryset=Repository.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)
        if 'export' in request.GET:
            cols = [('id','ID'), ('name','仓库名称'), ('type','仓库类型'), ('created_at','创建时间')]
            return export_queryset_to_excel(f.qs, cols, 'repositories')
        return render(request, 'repo/repository_list.html', {'filter': f, 'page_obj': objs})

# ---------- Repository Create View ----------
class RepositoryCreateView(View):
    def get(self, request):
        form = RepositoryForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = RepositoryForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

# ---------- Repository Update View ----------
class RepositoryUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Repository, pk=pk)
        form = RepositoryForm(instance=obj)
        return render_modal_form(request, form, context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Repository, pk=pk)
        form = RepositoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

# ---------- Repository Delete View ----------
class RepositoryDeleteView(DeleteView):
    model = Repository
    success_url = reverse_lazy('system:repository_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})
