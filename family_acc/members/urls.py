from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.list, name='list'),
    path('member_create/', views.member_create, name='member_create'),
    path('<uuid:uuid>/', views.member_edit, name='member_edit'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
