from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('create_expence', views. create_expence, name='create_expence')
]