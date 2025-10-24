from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification_list'),
    path('create/', views.NotificationCreateView.as_view(), name='notification_create'),
    path('<int:pk>/edit/', views.NotificationUpdateView.as_view(), name='notification_edit'),
    path('<int:pk>/delete/', views.NotificationDeleteView.as_view(), name='notification_delete'),
]