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
        read_only_fields = fields

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['date', 'account', 'amount', 'category', 'remark']

    def create(self, validated_data):
        user = self.context['request'].user
        account = validated_data['account']
        if( self.context['transaction_type'] == 'income'):
            amount = abs(validated_data.pop('amount'))
        else:
            amount = -abs(validated_data.pop('amount'))
            
        return Transaction.objects.create(
            **validated_data,
            created_by=user,
            family=user.profile.family,
            currency=account.currency,
            amount=amount,
        )
        
    def validate_amount(self, value):
        if value == 0:
            raise serializers.ValidationError("Account cannot be 0")
        return value
    
    # def validate(self, attrs):
    #     user = self.context['request'].user
    #     family = user.profile.family

    #     if attrs['account'].family != family:
    #         raise serializers.ValidationError({"account": "Invalid account"})
    #     if attrs['category'].family != family:
    #         raise serializers.ValidationError({"category": "Invalid category"})
        
        return attrs