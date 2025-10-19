# system/views/register_approval_view.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from system.models import User

from system.models.register_request import RegisterRequest


# @login_required
# @permission_required('auth.view_user', raise_exception=True)
def register_request_list(request):
    """注册申请列表"""
    status = request.GET.get('status', '')
    query = RegisterRequest.objects.all().order_by('-created_at')
    if status:
        query = query.filter(status=status)
    return render(request, 'system/accounts/register_approval_list.html', {'requests': query, 'status': status})


# @login_required
# @permission_required('auth.change_user', raise_exception=True)
def register_request_approve(request, pk):
    """审批通过"""
    print(f'pk is {pk}')
    req = get_object_or_404(RegisterRequest, pk=pk)

    if req.status != 'pending':
        messages.warning(request, "该申请已处理，无需重复操作。")
        return redirect('system:register_request_list')

    comment = request.POST.get('comment', '')
    print(f'content is {comment}')

    # 审批逻辑
    req.status = 'approved'
    req.comment = comment
    req.reviewer = request.user
    req.reviewed_at = timezone.now()
    req.save()

    print('fuck save here')
    # ✅ 创建正式用户（使用注册时的加密密码）
    if not User.objects.filter(username=req.phone).exists():
        User.objects.create(
            username=req.phone,
            first_name=req.name,
            password=req.password,  # 已加密
        )

    messages.success(request, f"已批准 {req.name} 的注册申请。")
    return redirect('system:register_request_list')


@login_required
@permission_required('auth.change_user', raise_exception=True)
def register_request_reject(request, pk):
    """审批拒绝"""
    req = get_object_or_404(RegisterRequest, pk=pk)

    if req.status != 'pending':
        messages.warning(request, "该申请已处理，无需重复操作。")
        return redirect('system:register_request_list')

    comment = request.POST.get('comment', '')

    req.status = 'rejected'
    req.comment = comment
    req.reviewer = request.user
    req.reviewed_at = timezone.now()
    req.save()

    messages.success(request, f"已拒绝 {req.name} 的注册申请。")
    return redirect('system:register_request_list')
