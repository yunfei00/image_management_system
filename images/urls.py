from django.urls import path
from . import views


app_name = 'images'

urlpatterns = [
    path('images/base/', views.BaseImageListView.as_view(), name='base_list'),
    path('images/base/create/', views.BaseImageCreateView.as_view(), name='base_create'),
    path('images/base/<int:pk>/edit/', views.BaseImageUpdateView.as_view(), name='base_edit'),
    path('images/base/<int:pk>/delete/', views.BaseImageDeleteView.as_view(), name='base_delete'),

    path('images/business/', views.BusinessImageListView.as_view(), name='biz_list'),
    path('images/business/create/', views.BusinessImageCreateView.as_view(), name='biz_create'),
    path('images/business/<int:pk>/edit/', views.BusinessImageUpdateView.as_view(), name='biz_edit'),
    path('images/business/<int:pk>/delete/', views.BusinessImageDeleteView.as_view(), name='biz_delete'),

]
