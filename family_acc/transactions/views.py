from django.shortcuts import render
from .models import Transaction

def transactions(request):
    transaction_data = Transaction.objects.all()
    return render(request, "transactions.html", {"data": transaction_data})
