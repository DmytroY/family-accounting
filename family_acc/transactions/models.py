from django.db import models
from django.contrib.auth.models import User

class Currency(models.Model):
    code = models.CharField(max_length=3)
    descr = models.CharField(max_length=255)

    def __str__(self):
        return self.code

class Account(models.Model):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    income_flag = models.BooleanField(null=True)
    expense_flag = models.BooleanField(null=True)

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    remark = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    family = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.date}  {self.account}  {self.amount}  {self.currency}  {self.category}"
