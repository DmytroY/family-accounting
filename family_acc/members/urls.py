from django.urls import path, include, reverse_lazy
from . import views, api_views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView


urlpatterns = [
    path("api/members/", api_views.MemberList.as_view(), name="api_members"),
    path("api/register/", api_views.RegisterAPIView.as_view(), name="api_register"),

    path('', views.list, name='list'),
    path('member_create/', views.member_create, name='member_create'),
    path('<uuid:uuid>/', views.member_edit, name='member_edit'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
