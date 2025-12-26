from django.contrib import admin
from .models import Currency, Account, Category, Transaction
import csv
from django.http import HttpResponse


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "family")

class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "balance", "currency", "family")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "income_flag", "expense_flag", "family")

# adding export Transactions to csv
@admin.action(description="Export selected as CSV")
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="transactions.csv"'
    writer = csv.writer(response)
    fields = [f.name for f in modeladmin.model._meta.fields]
    writer.writerow(fields)
    for obj in queryset:
        writer.writerow([getattr(obj, f) for f in fields])
    return response

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "account", "amount", "currency", "category", "remark", "family")
    actions = [export_as_csv]

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)

