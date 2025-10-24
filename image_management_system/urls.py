"""
URL configuration for image_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from detection.views import ProjectDetectToolViewSet, PreDetectViewSet, DetectDeviceViewSet, DetectCenterConfigViewSet
from images.views import BaseImageViewSet, BusinessImageViewSet
from notification.views import NotificationViewSet
from projects.views import ProjectViewSet
from repo.views import RepositoryViewSet
from system.views.approvals_views import ApprovalFlowViewSet
from system.views.departments import DepartmentViewSet
from system.views.roles import RoleViewSet
from system.views.post import PositionViewSet
from system.views.tools import ToolViewSet
from system.views.users import UserViewSet
from system.views.login_log import LoginLogViewSet
from system.views.menu import MenuViewSet
from system.views.oper_log import OperationLogViewSet


router = routers.DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('projects', ProjectViewSet)
router.register('roles', RoleViewSet)
router.register('positions', PositionViewSet)
router.register('users', UserViewSet)
router.register('detect-tools', ToolViewSet)
router.register('logs/login', LoginLogViewSet)
router.register('logs/operation', OperationLogViewSet)
router.register('menus', MenuViewSet)
router.register('images/base', BaseImageViewSet)
router.register('images/business', BusinessImageViewSet)
router.register('approval-flows', ApprovalFlowViewSet)
router.register('detect-tools', ProjectDetectToolViewSet)
router.register('pre-detection', PreDetectViewSet)
router.register('repositories', RepositoryViewSet)

router.register('detect-center/config', DetectCenterConfigViewSet)
router.register('detect-devices', DetectDeviceViewSet)

router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('system.urls', namespace='system')),
    path("images/", include("images.urls")),
    path("projects/", include("projects.urls")),
    path("detection/", include("detection.urls")),
    path("repo/", include("repo.urls")),
    path('notifications/', include("notification.urls", namespace="notifications")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/', include(router.urls)),
]
