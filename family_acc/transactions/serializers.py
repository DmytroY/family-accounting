from rest_framework import serializers
from . models import Currency, Account, Category, Transaction

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "code", "description"]

class AccountSerializer(serializers.ModelSerializer):
    # currency is foreign key for account, to show currency name(curency code) instead of id we need next
    currency = serializers.CharField(source="currency.code")

    class Meta:
        model = Account
        fields = ["id", "name", "balance", "currency"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "income_flag", "expense_flag"]

class TransactionSerializer(serializers.ModelSerializer):
    # account, currency, category, created_by are ferreign keys
    account = serializers.CharField(source="account.name")
    currency = serializers.CharField(source="currency.code")
    category = serializers.CharField(source="category.name")
    created_by = serializers.CharField(source="created_by.username")

    class Meta:
        model = Transaction
        fields = ["id", "date", "account", "amount", "currency", "category", "remark", "created_by"]

    
