from django.urls import path

from .views import departments
from .views.home import home

app_name = 'system'

urlpatterns = [
    path('', home, name='home'),

    # 部门管理
    path('dept/', departments.DeptListView.as_view(), name='dept_list'),
    path('dept/create/', departments.DeptCreateView.as_view(), name='dept_create'),
    path('dept/<int:pk>/edit/', departments.DeptUpdateView.as_view(), name='dept_edit'),
    path('dept/<int:pk>/delete/', departments.DeptDeleteView.as_view(), name='dept_delete'),
]
