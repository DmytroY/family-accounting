"""
URL configuration for family_acc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views, api_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [  
    path('admin/', admin.site.urls),

    path('i18n/', include('django.conf.urls.i18n')),

    path("api/token/", obtain_auth_token),
    path("api/token/regenerate/", api_views.regenerate_token),


    path('', views.home, name='home'),
    path('test', views.test, name='test'),
    path('members/', include(('members.urls', 'members'), namespace='members')),
    path('transactions/', include(('transactions.urls', 'transactions'), namespace='transactions')), 
    path("accounts/", include("django.contrib.auth.urls")),
]
