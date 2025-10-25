from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView
from rest_framework import viewsets

from system.filters.user_filter import UserFilter
from system.forms import UserForm, AdminResetPasswordForm
from system.models import User
from system.serializers.user import UserSerializer
from system.utils import export_queryset_to_excel
from system.views.handle_modal_form import render_modal_form


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ---------- User ----------
class UserListView(View):
    def get(self, request):
        # if request.user.roles.name != "超级管理员":
        #     print('无权访问用户列表')
        #     return HttpResponseForbidden("你没有权限访问此页面")
        print(f'request get is {request.GET}')
        f = UserFilter(request.GET, queryset=User.objects.select_related('department').prefetch_related('role').all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        # ✅ 打印所有用户信息（分页后的）
        print("=== 用户列表调试输出 ===")
        print('objs type', type(objs))
        print('objs is', objs)
        # for u in objs:
        #     role_names = ", ".join([r.username for r in u.roles.all()]) or "无角色"
        #     dept_name = u.dept.name if u.dept else "无部门"
        #     status_display = u.get_status_display() if hasattr(u, 'get_status_display') else u.status
        #     print(f"ID: {u.id} | 用户名: {u.username} | 姓名: {u.name} | 公司: {u.company or '无'} | "
        #           f"部门: {dept_name} | 角色: {role_names} | 状态: {status_display}")
        # print("=======================")

        # if 'export' in request.GET:
        #     cols = [('id','ID'), ('name','用户名称'), ('phone','手机号'), ('company','公司'),('dept','部门'), ('roles','角色'), ('status','状态')]
        #     return export_queryset_to_excel(f.qs, cols, 'users')

        return render(request, 'system/user_list.html', {'filter': f, 'page_obj': objs})

class UserCreateView(View):
    def get(self, request):
        return render_modal_form(request, UserForm())

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # form.save_m2m()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class UserUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(User, pk=pk)
        return render_modal_form(request, UserForm(instance=obj), context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # form.save_m2m()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class UserDeleteView(DeleteView):
    model = User
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})

class AdminResetPasswordView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    管理员为用户重置密码（需要有变更用户的权限）
    """
    permission_required = 'auth.change_user'   # 如果你自定义User模型，换成对应app_label.codename

    def get(self, request, pk):
        print('receive reset password')
        target = get_object_or_404(User, pk=pk)
        # 传递 user 参数而非 instance，初始化 AdminResetPasswordForm
        form = AdminResetPasswordForm(user=target)
        # 使用 render_modal_form 渲染模态框内容
        return render_modal_form(request, form, context_extra={'target': target})

    def post(self, request, pk):
        target = get_object_or_404(User, pk=pk)
        form = AdminResetPasswordForm(request.POST, user=target)
        if form.is_valid():
            # 保存新密码
            new_password = form.cleaned_data['new_password']
            target.set_password(new_password)
            target.save()
            return JsonResponse({'success': True, 'message': '密码重置成功'})

        # 如果表单无效，返回错误的表单HTML
        html = render_to_string('system/user_list.html', {'form': form, 'target': target}, request=request)
        return JsonResponse({'success': False, 'html': html})

class UserDetailView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'system/user_detail.html', {'user': user})