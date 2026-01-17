from django import forms
from . import models

class CreateAccount(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ['name','balance','currency']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['currency'].queryset = (
                models.Currency.objects
                .filter(family=user.profile.family)
                .order_by('code')
            )


class CreateCurrency(forms.ModelForm):
    class Meta:
        model = models.Currency
        fields = ['code','description']


class CreateCategory(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name','income_flag','expense_flag']


class CreateTransactionBase(forms.ModelForm):
    currency = forms.ModelChoiceField(queryset=models.Currency.objects.none())
    category_flag = None # derived class defines 'income_flag' or 'expense_flag'

    class Meta:
        model = models.Transaction
        fields = ['date', 'currency', 'account', 'amount', 'category', 'remark']
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 2, 'required': False}),
        }

    def clean_amount(self):
        value = self.cleaned_data['amount']
        if value == 0:
            raise forms.ValidationError("Amount cannot be 0")
        return value

    # custom constructror. required to implement logic
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        family = user.profile.family

        # nitialize base ModelForm
        super().__init__(*args, **kwargs)
        
        self.fields['currency'].queryset = models.Currency.objects.filter(family=family)
        self.fields["account"].queryset = models.Account.objects.none()        # hide all accounts until currency selected
        self.fields['category'].queryset = models.Category.objects.filter(family=family, **{self.category_flag: True}).order_by('name')

        if "currency" in self.data:
            try:
                # get currency id from POST data
                currency_id = int(self.data.get("currency"))
                self.fields['account'].queryset =  models.Account.objects.filter(family=family, currency_id=currency_id)
            except (TypeError, ValueError):
                # don’t crash form rendering if user submits form without selecting currency or frontend error happens.
                pass
        elif self.instance.pk:
            self.fields["account"].queryset = models.Account.objects.filter(family=family, currency=self.instance.currency)

class CreateExpense(CreateTransactionBase):
    category_flag = 'expense_flag'

class CreateIncome(CreateTransactionBase):
    category_flag = 'income_flag'


class UploadAccounts(forms.Form):
    file = forms.FileField()

class UploadCategory(forms.Form):
    file = forms.FileField()

class UploadTransaction(forms.Form):
    file = forms.FileField()