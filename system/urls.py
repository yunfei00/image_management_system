from django.urls import path

from .views import departments, roles
from .views.home import home

app_name = 'system'

urlpatterns = [
    path('', home, name='home'),

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

]
