from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('edit/<id>', views.edit, name='edit'),
    # path('delete/<id>', views.delete, name='delete'),
    path('create_expense', views. create_expense, name='create_expense'),
    path('create_income', views. create_income, name='create_income'),
    path('create_account', views. create_account, name='create_account'),
    path('list_accounts', views. list_accounts, name='list_accounts'),
]