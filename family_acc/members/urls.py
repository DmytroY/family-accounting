from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('member_create/', views.member_create, name='member_create'),
    path('<uuid:uuid>/', views.details, name='details'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
