from django.urls import path

from .views import departments, roles, post, users
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

]
