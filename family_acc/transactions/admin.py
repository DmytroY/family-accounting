from django.contrib import admin
from .models import Currency, Account, Category, Transaction

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "descr")

class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "balance")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "income_flag", "expence_flag",)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "account", "amount", "currency", "category", "remark")

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
