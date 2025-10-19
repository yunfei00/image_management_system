"""
用户登录视图
"""

# system/views/auth_views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    """用户登录"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "登录成功！")
            return redirect('system:home')  # 登录成功后跳转到首页
        else:
            messages.error(request, "用户名或密码错误！")

    return render(request, 'system/accounts/login.html')


def logout_view(request):
    """退出登录"""
    logout(request)
    return redirect('system:login')
