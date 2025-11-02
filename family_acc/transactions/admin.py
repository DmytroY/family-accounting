from django.contrib import admin
from .models import Account, Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "account", "amount",)

admin.site.register(Account)
admin.site.register(Transaction, TransactionAdmin)
