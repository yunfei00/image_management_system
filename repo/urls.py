from django.urls import path
from . import views

app_name = 'repo'

urlpatterns = [
    # 仓库列表
    path('repo/', views.RepositoryListView.as_view(), name='repo_list'),

    # 新建仓库
    path('repo/create/', views.RepositoryCreateView.as_view(), name='repo_create'),

    # 编辑仓库
    path('repo/<int:pk>/edit/', views.RepositoryUpdateView.as_view(), name='repo_edit'),

    # 删除仓库
    path('repo/<int:pk>/delete/', views.RepositoryDeleteView.as_view(), name='repo_delete'),
]
