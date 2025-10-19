# system/views/login_log_view.py
import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from system.filters.login_log_filter import LoginLogFilter
from system.serializers.login_log_serializer import LoginLogSerializer

from rest_framework import viewsets, filters
from system.models import LoginLog
from django_filters.rest_framework import DjangoFilterBackend

from system.utils import export_queryset_to_excel


class LoginLogViewSet(viewsets.ModelViewSet):
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'username', 'ip']
    search_fields = ['username', 'ip', 'result']
    ordering_fields = ['login_time']
#
# class LoginLogViewSet(viewsets.ModelViewSet):
#     queryset = LoginLog.objects.all().order_by('-login_time')
#     serializer_class = LoginLogSerializer
#     # permission_classes = [IsAuthenticated]
#     permission_classes = [AllowAny]  # 关键配置：允许所有用户访问（包括未登录）
#
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['status', 'username', 'ip']
#     search_fields = ['username', 'ip', 'result']
#     ordering_fields = ['login_time']
#
#     def get_queryset(self):
#         # 可根据时间范围筛选
#         queryset = super().get_queryset()
#         start_time = self.request.query_params.get('start_time')
#         end_time = self.request.query_params.get('end_time')
#         if start_time and end_time:
#             queryset = queryset.filter(login_time__range=[start_time, end_time])
#         return queryset


class LoginLogListView(View):

    def get(self, request):
        print(f'login log is {request.GET}')
        f = LoginLogFilter(request.GET, queryset=LoginLog.objects.all())
        qs = f.qs.order_by('-login_time')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)

        # 导出 Excel 功能
        if 'export' in request.GET:
            cols = [
                ('username', '用户名'),
                ('login_time', '登录时间'),
                ('ip', '登录IP'),
                ('status', '状态'),
                ('result', '登录结果'),
            ]
            return export_queryset_to_excel(f.qs, cols, 'login_logs')

        return render(request, 'system/login_log_list.html', {
            'filter': f,
            'page_obj': objs,
        })


class LoginLogDeleteView(DeleteView):
    model = LoginLog
    success_url = reverse_lazy('system:login_log_list')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})