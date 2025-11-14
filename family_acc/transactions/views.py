from django.shortcuts import render, redirect
from .models import Transaction, Account
from django.contrib.auth.decorators import login_required
from . import forms
from django.utils import timezone

@login_required(login_url="/members/login/")
def list(request):
    user = request.user
    transaction_data = Transaction.objects.filter(family= getattr(user.profile, 'family', None)).order_by('-id').order_by('-date', '-id')[:20]
    return render(request, "list.html", {"data": transaction_data})

@login_required(login_url="/members/login/")
def edit(request, id):
    transaction = Transaction.objects.get(id=id)
    if request.POST.get("action") == "delete":
        transaction.delete()
        return redirect('transactions:list')
    
    if request.POST.get("action") == "cansel":
        return redirect('transactions:list')
    
    if transaction.amount >= 0:
        # treat it as income
        if request.method == "POST":
            form = forms.CreateIncome(request.POST, instance=transaction)
            if form.is_valid():
                income = form.save(commit=False)
                income.created_by = request.user
                income.amount = abs(income.amount)
                income.save()
                return redirect('transactions:list')
        else:
            form = forms.CreateIncome(instance=transaction)
        
    else:
        # treat it as expense
        if request.method == "POST":
            form = forms.CreateExpense(request.POST, instance=transaction)
            if form.is_valid():
                expense = form.save(commit=False)
                expense.created_by = request.user
                expense.amount = -abs(expense.amount)
                expense.save()
                return redirect('transactions:list')
        else:
            form = forms.CreateExpense(instance=transaction)

    return render(request, "edit_transaction.html", {'form': form, 'transaction': transaction})

@login_required(login_url="/members/login/")
def create_expense(request):
    if(request.method == "POST"):
        form = forms.CreateExpense(request.POST, user=request.user)
        if form.is_valid():
            # save
            new_expense = form.save(commit=False)
            new_expense.created_by = request.user
            # expenses always shoud be saved as negative amount transaction
            new_expense.amount = -abs(new_expense.amount)
            new_expense.save()
            return redirect('transactions:list')
    else:
        form = forms.CreateExpense(initial={'date': timezone.now().date()}, user=request.user)
    return render(request, 'create_expense.html', {'form': form})

@login_required(login_url="/members/login/")
def create_income(request):
    if(request.method == "POST"):
        form = forms.CreateIncome(request.POST)
        if form.is_valid():
            # save
            new_income = form.save(commit=False)
            new_income.created_by = request.user
            # income always shoud be saved as positive amount transaction
            new_income.amount = abs(new_income.amount)
            new_income.save()
            return redirect('transactions:list')
    else:
        form = forms.CreateIncome(initial={'date': timezone.now().date()})
    return render(request, 'create_income.html', {'form': form})

@login_required(login_url="/members/login/")
def create_account(request):
    if request.method == "POST":
        form = forms.CreateAccount(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.family = request.user.profile.family
            new_account.save()
            return redirect('transactions:list_accounts')
    else:
        form = forms.CreateAccount()
    return render(request, 'create_account.html',  {'form': form})

@login_required(login_url="/members/login/")
def list_accounts(request):
    user = request.user
    accounts_data = Account.objects.filter(family= getattr(user.profile, 'family', None)).order_by('name')
    return render(request, "list_accounts.html", {"data": accounts_data})

