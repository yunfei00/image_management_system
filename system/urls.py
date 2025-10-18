from django.urls import path
from .views.home import home

app_name = 'system'

urlpatterns = [
    path('', home, name='home'),
]
