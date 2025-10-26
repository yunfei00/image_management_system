from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path("dashboard/", views.UserDashboardView.as_view(), name="user_dashboard"),
    path("list/", views.ProjectListView.as_view(), name="project_list"),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
    path("<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project_delete"),
]
