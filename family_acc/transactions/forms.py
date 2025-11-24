from django import forms
from . import models

class CreateAccount(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ['name','balance','currency']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['currency'].queryset =  models.Currency.objects.filter(family=user.profile.family).order_by('code')

class CreateCurrency(forms.ModelForm):
    class Meta:
        model = models.Currency
        fields = ['code','description']

class CreateCategory(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name','income_flag','expense_flag']

class CreateExpense(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['date', 'account', 'amount', 'category', 'remark']
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 2, 'required': False}),
        }

    def clean_amount(self):
        value = self.cleaned_data['amount']
        if value == 0:
            raise forms.ValidationError("Amount cannot be 0")
        return value

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = models.Account.objects.filter(family=user.profile.family).order_by('name')
        self.fields['category'].queryset = models.Category.objects.filter(family=user.profile.family, expense_flag=True).order_by('name')


class CreateIncome(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['date', 'account', 'amount', 'category', 'remark']
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 2, 'required': False}),
        }

    def clean_amount(self):
        value = self.cleaned_data['amount']
        if value == 0:
            raise forms.ValidationError("Amount cannot be 0")
        return value
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset =  models.Account.objects.filter(family=user.profile.family).order_by('name')
        self.fields['category'].queryset = models.Category.objects.filter(family=user.profile.family, income_flag=True).order_by('name')