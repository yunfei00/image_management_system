from django.urls import path
from . import views

app_name = 'repo'

urlpatterns = [
    path('', views.home, name='home'),
]

