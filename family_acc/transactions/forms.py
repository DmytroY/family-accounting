from django import forms
from . import models

class CreateExpense(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['date', 'account', 'amount', 'currency', 'category', 'remark']
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = models.Account.objects.order_by('name')
        self.fields['currency'].queryset = models.Currency.objects.order_by('code')
        self.fields['category'].queryset = models.Category.objects.filter(expense_flag=True).order_by('name')

class CreateIncome(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['date', 'account', 'amount', 'currency', 'category', 'remark']
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = models.Account.objects.order_by('name')
        self.fields['currency'].queryset = models.Currency.objects.order_by('code')
        self.fields['category'].queryset = models.Category.objects.filter(income_flag=True).order_by('name')