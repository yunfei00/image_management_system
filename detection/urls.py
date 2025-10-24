from django.urls import path
from . import views

app_name = 'detection'

urlpatterns = [
    # 检测工具
    # path('tool/', views.DetectToolListView.as_view(), name='tool_list'),
    # path('tool/create/', views.DetectToolCreateView.as_view(), name='tool_create'),
    # path('tool/<int:pk>/edit/', views.DetectToolUpdateView.as_view(), name='tool_edit'),
    # path('tool/<int:pk>/delete/', views.DetectToolDeleteView.as_view(), name='tool_delete'),

    # 项目-检测工具（检测策略）
    path('project-tool/', views.ProjectDetectToolListView.as_view(), name='project_tool_list'),
    path('project-tool/create/', views.ProjectDetectToolCreateView.as_view(), name='project_tool_create'),
    path('project-tool/<int:pk>/edit/', views.ProjectDetectToolUpdateView.as_view(), name='project_tool_edit'),
    path('project-tool/<int:pk>/delete/', views.ProjectDetectToolDeleteView.as_view(), name='project_tool_delete'),

    # 预检测记录
    path('pre-detect/', views.PreDetectListView.as_view(), name='pre_detect_list'),
    path('pre-detect/create/', views.PreDetectCreateView.as_view(), name='pre_detect_create'),
    path('pre-detect/<int:pk>/edit/', views.PreDetectUpdateView.as_view(), name='pre_detect_edit'),
    path('pre-detect/<int:pk>/delete/', views.PreDetectDeleteView.as_view(), name='pre_detect_delete'),

    # 检测中心配置
    path('center/config/', views.CenterConfigListView.as_view(), name='center_config_list'),
    path('center/config/create/', views.CenterConfigCreateView.as_view(), name='center_config_create'),
    path('center/config/<int:pk>/edit/', views.CenterConfigUpdateView.as_view(), name='center_config_edit'),
    path('center/config/<int:pk>/delete/', views.CenterConfigDeleteView.as_view(), name='center_config_delete'),

    # 检测设备
    path('devices/', views.DeviceListView.as_view(), name='device_list'),
    path('devices/create/', views.DeviceCreateView.as_view(), name='device_create'),
    path('devices/<int:pk>/edit/', views.DeviceUpdateView.as_view(), name='device_edit'),
    path('devices/<int:pk>/delete/', views.DeviceDeleteView.as_view(), name='device_delete'),

]





