from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path("list/", views.ProjectListView.as_view(), name="project_list"),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
    path("<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project_delete"),
]
