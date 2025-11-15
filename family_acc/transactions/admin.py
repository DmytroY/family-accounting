from django.contrib import admin
from .models import Currency, Account, Category, Transaction

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "description", 'family')

class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "balance", 'family')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "income_flag", "expense_flag", 'family')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "account", "amount", "currency", "category", "remark", 'family')

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
