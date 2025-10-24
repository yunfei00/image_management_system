# notifications/views.py
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets

from notification.filters.notification_filter import NotificationFilter
from notification.forms import NotificationForm
from notification.models import Notification
from notification.serializers.notification import NotificationSerializer
from system.utils import export_queryset_to_excel
from system.views.handle_modal_form import render_modal_form


# ---- API ----
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer


# ---- Web ----
class NotificationListView(View):
    def get(self, request):
        f = NotificationFilter(request.GET, queryset=Notification.objects.filter(user=request.user))
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)

        # 导出
        if 'export' in request.GET:
            cols = [('id','ID'), ('title','标题'), ('type','类型'), ('status','状态'), ('created_at','时间')]
            return export_queryset_to_excel(f.qs, cols, 'notifications')

        return render(request, 'notifications/notification_list.html', {'filter': f, 'page_obj': objs})


class NotificationCreateView(View):
    def get(self, request):
        form = NotificationForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)


class NotificationUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Notification, pk=pk)
        form = NotificationForm(instance=obj)
        return render_modal_form(request, form, context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Notification, pk=pk)
        form = NotificationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})


class NotificationDeleteView(DeleteView):
    model = Notification
    success_url = reverse_lazy('notifications:notification_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})
