from django.shortcuts import render
from .models import Transaction
from django.contrib.auth.decorators import login_required

@login_required(login_url="/members/login/")
def list(request):
    transaction_data = Transaction.objects.all()
    return render(request, "list.html", {"data": transaction_data})
