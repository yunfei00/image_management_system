from django.urls import path
from . import views


app_name = 'images'

urlpatterns = [
    # path('upload/', views.upload_business_image, name='biz_create'),
    path('images/base/', views.BaseImageListView.as_view(), name='base_list'),
    path('base_image/download/<int:image_id>/', views.base_image_download, name='base_download'),
    path('base_image/details/<int:image_id>/', views.base_image_details, name='base_details'),
    path('images/base/create/', views.BaseImageCreateView.as_view(), name='base_create'),
    path('images/base/<int:pk>/edit/', views.BaseImageUpdateView.as_view(), name='base_edit'),
    path('images/base/<int:pk>/delete/', views.BaseImageDeleteView.as_view(), name='base_delete'),

    path('business/', views.BusinessImageListView.as_view(), name='biz_list'),
    path('business_image/download/<int:image_id>/', views.business_image_download, name='business_download'),
    path('business_image/details/<int:image_id>/', views.business_image_details, name='business_details'),
    path('business/create/', views.BusinessImageCreateView.as_view(), name='biz_create'),
    path('business/<int:pk>/edit/', views.BusinessImageUpdateView.as_view(), name='biz_edit'),
    path('business/<int:pk>/delete/', views.BusinessImageDeleteView.as_view(), name='biz_delete'),

]
