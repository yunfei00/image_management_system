from django.urls import path

from .views import (departments, roles, post, users, tools, login_log, oper_log, register,
                    register_approval_view, auth_views, menu)
from .views.home import home
from .views.menu import MenuUpdateView, MenuDeleteView

app_name = 'system'

urlpatterns = [
    path('', home, name='home'),

    path('register/', register.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    # path('applications/', accounts_views.application_list, name='application_list'),
    # path('applications/approve/<int:app_id>/', accounts_views.approve_application, name='approve_application'),
    # path('applications/reject/<int:app_id>/', accounts_views.reject_application, name='reject_application'),
    path("", home, name="home"),
    path('register/requests/', register_approval_view.register_request_list,
         name='register_request_list'),
    path('register/approve/<int:pk>/', register_approval_view.register_request_approve,
         name='register_request_approve'),
    path('register/reject/<int:pk>/', register_approval_view.register_request_reject,
         name='register_request_reject'),

    # 部门管理
    path('dept/', departments.DeptListView.as_view(), name='dept_list'),
    path('dept/create/', departments.DeptCreateView.as_view(), name='dept_create'),
    path('dept/<int:pk>/edit/', departments.DeptUpdateView.as_view(), name='dept_edit'),
    path('dept/<int:pk>/delete/', departments.DeptDeleteView.as_view(), name='dept_delete'),

    # 角色管理
    path('role/', roles.RoleListView.as_view(), name='role_list'),
    path('role/create/', roles.RoleCreateView.as_view(), name='role_create'),
    path('role/<int:pk>/edit/', roles.RoleUpdateView.as_view(), name='role_edit'),
    path('role/<int:pk>/delete/', roles.RoleDeleteView.as_view(), name='role_delete'),

    # 岗位管理
    path('post/', post.PostListView.as_view(), name='post_list'),
    path('post/create/', post.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', post.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', post.PostDeleteView.as_view(), name='post_delete'),

    # 用户管理
    path('user/', users.UserListView.as_view(), name='user_list'),
    path('user/create/', users.UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/edit/', users.UserUpdateView.as_view(), name='user_edit'),
    path('user/<int:pk>/delete/', users.UserDeleteView.as_view(), name='user_delete'),

    # 检测工具管理
    path('tool/', tools.ToolListView.as_view(), name='tool_list'),
    path('tool/create/', tools.ToolCreateView.as_view(), name='tool_create'),
    path('tool/<int:pk>/edit/', tools.ToolUpdateView.as_view(), name='tool_edit'),
    path('tool/<int:pk>/delete/', tools.ToolDeleteView.as_view(), name='tool_delete'),

    # 日志管理
    path('loginlog/', login_log.LoginLogListView.as_view(), name='login_log_list'),
    path('loginlog/<int:pk>/delete/', login_log.LoginLogDeleteView.as_view(), name='login_log_delete'),

    path('operationlog/', oper_log.OperationLogListView.as_view(), name='oper_log_list'),
    path('operationlog/<int:pk>/delete/', login_log.LoginLogDeleteView.as_view(), name='oper_log_delete'),
# 菜单管理
    path('menus/', menu.MenuListView.as_view(), name='menu_list'),
    path('menus/create/', menu.MenuCreateView.as_view(), name='menu_create'),
    path('menus/<int:pk>/edit/', MenuUpdateView.as_view(), name='menu_edit'),
    path('menus/<int:pk>/delete/', MenuDeleteView.as_view(), name='menu_delete'),
]
