from django import forms
from . import models

class CreateExpence(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['date', 'account', 'amount', 'currency', 'category', 'remark']