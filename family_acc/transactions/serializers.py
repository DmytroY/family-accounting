from rest_framework import serializers
from . models import Currency, Account

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["code", "description"]

class AccountSerializer(serializers.ModelSerializer):
    # currency is foreign key for account, to show currency name(curency code) instead of id we need next
    currency = serializers.CharField(source="currency.code")

    class Meta:
        model = Account
        fields = ["name", "balance", "currency"]
