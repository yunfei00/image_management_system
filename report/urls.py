from django.urls import path, include
from . import views

urlpatterns = [
    # API接口
    # path('api/reports/', views.ReportViewSet.as_view({'get': 'list', 'post': 'create'}), name='report-list'),
    # path('api/reports/<int:pk>/',
    #      views.ReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='report-detail'),

    # 前端视图
    path('reports/', views.ReportListView.as_view(), name='report-list'),
    path('reports/create/', views.ReportCreateView.as_view(), name='report-create'),
    path('reports/update/<int:pk>/', views.ReportUpdateView.as_view(), name='report-update'),
    path('reports/delete/<int:pk>/', views.ReportDeleteView.as_view(), name='report-delete'),
]
