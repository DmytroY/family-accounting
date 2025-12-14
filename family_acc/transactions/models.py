from django.db import models
from django.contrib.auth.models import User

class Currency(models.Model):
    code = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    family = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code}"

class Account(models.Model):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    family = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'currency'], name='unique_name_currency')
        ]

    def __str__(self):
        return f"{self.name} ({self.currency})"
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    income_flag = models.BooleanField(default=False)
    expense_flag = models.BooleanField(default=False)
    family = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
    
class Transaction(models.Model):
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    remark = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    family = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date}  {self.account}  {self.amount}  {self.currency}  {self.category}"
