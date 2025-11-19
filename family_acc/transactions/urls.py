from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('transaction_list', views.transaction_list, name='transaction_list'),
    path('transaction_edit/<id>', views.transaction_edit, name='transaction_edit'),
    path('transaction_create_expense', views.transaction_create_expense, name='transaction_create_expense'),
    path('transaction_create_income', views.transaction_create_income, name='transaction_create_income'),
    
    path('account_list', views.account_list, name='account_list'),
    path('account_create', views.account_create, name='account_create'),
    path('account_edit/<id>', views.account_edit, name='account_edit'),

    path('currency_list', views.currency_list, name='currency_list'),
    path('currency_create', views.currency_create, name='currency_create'),
    path('currency_edit/<id>', views.currency_edit, name='currency_edit'),

    path('category_list', views.category_list, name='category_list'),
    path('category_create', views.category_create, name='category_create'),
    path('category_edit/<id>', views.category_edit, name='category_edit'),

    path("ajax/account/<int:account_id>/currency/", views.get_account_currency, name="ajax_account_currency")
]