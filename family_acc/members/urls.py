from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

# app_name = "members"

urlpatterns = [
    path('', views.list, name='list'),
    path('member_create/', views.member_create, name='member_create'),
    path('<uuid:uuid>/', views.details, name='details'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


#     # custom named routes inside "members"
#     path("password-reset/", 
#          auth_views.PasswordResetView.as_view(success_url=reverse_lazy('members:password_reset_done')),
#          name="password_reset"),

#     path("password-reset/done/",
#          auth_views.PasswordResetDoneView.as_view(),
#          name="password_reset_done"),

#     path("reset/<uidb64>/<token>/",
#          auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('members:password_reset_complete')),
#          name="password_reset_confirm"),

#     path("reset/done/",
#          auth_views.PasswordResetCompleteView.as_view(),
#          name="password_reset_complete"),
]
