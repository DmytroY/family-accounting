from django.urls import path
from . import views

urlpatterns = [
    path('testing/', views.testing, name='testing'),
    path('', views.list, name='list'),
    path('<slug:slug>', views.details, name='details'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
