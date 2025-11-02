from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    date = models.DateField(null=False)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.date}  {self.account}  {self.amount}"
