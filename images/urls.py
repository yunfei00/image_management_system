from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('', views.home, name='home'),
    # path('base/', views.BaseImageListView.as_view(), name='base_image_list'),
    # path('business/', views.business_image_list, name='business_image_list'),
    # path('base/add/', views.add_base_image, name='add_base_image'),
    # path('business/add/', views.add_business_image, name='add_business_image'),
    # # path('base/', views.base_image_list, name='base_image_list'),
    # path('base/download/<str:image_id>/', views.download_base_image, name='download_base_image'),
]
