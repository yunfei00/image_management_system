from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.utils import timezone

from system.models import Role, Position
from system.models.register_request import RegisterRequest


def register_view(request):
    roles = Role.objects.filter(status=1)
    positions = Position.objects.filter(status=1)

    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        company = request.POST.get("company")  # 新增字段
        position_id = request.POST.get("position")
        role_id = request.POST.get("role")   # 单选角色
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # 保留用户输入的数据
        context = {
            "username": username,
            "phone": phone,
            "company": company,  # 保存公司名称
            "position_id": int(position_id) if position_id else None,
            "role_id": int(role_id) if role_id else None,
            "positions": positions,
            "roles": roles,
        }

        print('current data is {}'.format(context))

        # 密码不一致
        if password != password2:
            messages.error(request, "两次密码输入不一致，请重新输入。")
            return render(request, "system/accounts/register.html", context)

        # 用户名重复
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            messages.error(request, "该用户名已存在，请更换用户名。")
            return render(request, "system/accounts/register.html", context)

        # # 1️⃣ 检查是否已存在于用户表
        # if User.objects.filter(phone=phone).exists():
        #     messages.error(request, "该手机号已存在，请直接登录。")
        #     return redirect('register_request')

        # 2️⃣ 检查是否在注册表中
        existing_req = RegisterRequest.objects.filter(name=username).order_by('-created_at').first()
        if existing_req:
            if existing_req.status == 'pending':
                messages.warning(request, "您的注册申请正在审批中，请耐心等待。")
                return redirect('register_request')
            elif existing_req.status == 'approved':
                messages.warning(request, "该用户已注册，请直接登录。")
                return redirect('register_request')
            elif existing_req.status == 'rejected':
                # 允许重新申请，覆盖旧记录
                existing_req.name = username
                existing_req.company = company
                existing_req.position_id = position_id
                existing_req.role_id = role_id
                existing_req.status = 'pending'
                existing_req.created_at = timezone.now()
                existing_req.save()
                messages.success(request, "您的重新申请已提交，请等待管理员审批。")
                return redirect('system:user_list')

        # position = Position.objects.filter(id=position_id).first()
        # role = Role.objects.filter(id=role_id).first()
        print('start register')
        RegisterRequest.objects.create(
            name=username,
            phone=phone,
            company=company,  # 保存公司名称
            position_id=position_id,
            role_id=role_id,
            password=make_password(password),  # ✅ 加密存储
        )
        print('finish register')
        messages.success(request, "注册申请已提交，请等待管理员审批。")
        print('change to user list')
        return redirect('system:dept_list')

    roles = Role.objects.exclude(name='超级管理员')
    positions = Position.objects.all()
    return render(request, "system/accounts/register.html", {"positions": positions, "roles": roles})


def register_approval_view(request, pk):
    req = RegisterRequest.objects.get(pk=pk)
    action = request.POST.get('action')  # approve / reject
    comment = request.POST.get('comment', '')
    req.reviewer = request.user
    req.reviewed_at = timezone.now()
    req.comment = comment

    if action == 'approve':
        req.status = 'approved'
        # 自动创建系统账户
        user = User.objects.create_user(
            username=req.phone,
            password='123456',  # 初始密码
            first_name=req.name,
        )
        user.role = req.role
        user.save()
        # 这里可以添加通知逻辑（短信 / 邮件）
    else:
        req.status = 'rejected'
    req.save()
    messages.success(request, f"审批已{ '通过' if action == 'approve' else '拒绝' }。")
    return redirect('register_request_list')

# def register_view(request):
#     # 🚀 先从数据库读取所有启用状态的部门和角色
#     depts = Department.objects.filter(status=1)
#     roles = Role.objects.filter(status=1)
#
#     if request.method == "POST":
#         username = request.POST.get("username")
#         phone = request.POST.get("phone")
#         dept_id = request.POST.get("dept")
#         role_id = request.POST.get("role")
#         password = request.POST.get("password")
#         password2 = request.POST.get("password2")
#
#         if password != password2:
#             messages.error(request, "两次输入的密码不一致。")
#         elif User.objects.filter(username=username).exists():
#             messages.error(request, "该用户名已存在。")
#         else:
#             dept = Department.objects.get(id=dept_id)
#             role = Role.objects.get(id=role_id)
#             user = User.objects.create_user(
#                 username=username,
#                 name=username,
#                 phone=phone,
#                 dept=dept,
#                 status=0  # 注册后默认停用
#             )
#             user.set_password(password)
#             user.save()
#             user.roles.add(role)
#             messages.success(request, "注册成功，请等待管理员审批。")
#             return redirect("system:login")
#
#     # 🚨 无论是否 POST，都要返回 depts 和 roles
#     return render(request, "system/accounts/register.html", {"depts": depts, "roles": roles})

def is_admin(user):
    return hasattr(user, 'roles') and user.roles.filter(name='管理员').exists()


@login_required
@user_passes_test(is_admin)
def application_list(request):
    """管理员审批页面"""
    apps = UserApplication.objects.all().order_by('-create_time')
    return render(request, 'system/accounts/../templates/system/accounts/application_list.html', {'apps': apps})


@login_required
@user_passes_test(is_admin)
def approve_application(request, app_id):
    app = get_object_or_404(UserApplication, id=app_id)
    if app.status == 'pending':
        user = User.objects.create(
            name=app.name,
            phone=app.phone,
            dept=app.dept,
            status=1  # 启用
        )
        user.roles.set(app.roles.all())
        user.save()
        app.status = 'approved'
        app.save()
        messages.success(request, f'用户 {user.name} 审核通过并已创建。')
    return redirect('application_list')


@login_required
@user_passes_test(is_admin)
def reject_application(request, app_id):
    app = get_object_or_404(UserApplication, id=app_id)
    if app.status == 'pending':
        app.status = 'rejected'
        app.save()
        app.delete()
        messages.warning(request, f'用户 {app.name} 申请已拒绝并删除。')
    return redirect('application_list')


# def login_view1(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             if not user.is_active:
#                 messages.error(request, '您的账号尚未通过管理员审核。')
#                 return redirect('login')
#             login(request, user)
#             return redirect('system:dept_list')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'system/accounts/login.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f'user status is {user.status}')
            if user.status == 1:
                login(request, user)
                return redirect('system:dashboard')
                # return redirect("index")
            else:
                messages.error(request, "账户未启用，请联系管理员。")
        else:
            messages.error(request, "用户名或密码错误。")

        # 🚨 注意这里用 render，而不是 redirect！
        # redirect 会清除 messages
        return render(request, "system/accounts/login.html")

    return render(request, "system/accounts/login.html")
#
# def logout_view(request):
#     logout(request)
#     return redirect('system:login')
