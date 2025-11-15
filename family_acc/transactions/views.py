from django.shortcuts import render, redirect
from .models import Transaction, Account, Currency, Category
from django.contrib.auth.decorators import login_required
from . import forms
from django.utils import timezone

@login_required(login_url="/members/login/")
def transaction_list(request):
    user = request.user
    transaction_data = Transaction.objects.filter(family= getattr(user.profile, 'family', None)).order_by('-id').order_by('-date', '-id')[:20]
    return render(request, "transaction_list.html", {"data": transaction_data})

@login_required(login_url="/members/login/")
def transaction_edit(request, id):
    transaction = Transaction.objects.get(id=id)
    if request.POST.get("action") == "delete":
        transaction.delete()
        return redirect('transactions:transaction_list')
    
    if request.POST.get("action") == "cansel":
        return redirect('transactions:transaction_list')
    
    if transaction.amount >= 0:
        # treat it as income
        if request.method == "POST":
            form = forms.CreateIncome(request.POST, instance=transaction, user=request.user)
            if form.is_valid():
                income = form.save(commit=False)
                income.created_by = request.user
                income.amount = abs(income.amount)
                income.save()
                return redirect('transactions:transaction_list')
        else:
            form = forms.CreateIncome(instance=transaction, user=request.user)
        
    else:
        # treat it as expense
        if request.method == "POST":
            form = forms.CreateExpense(request.POST, instance=transaction, user=request.user)
            if form.is_valid():
                expense = form.save(commit=False)
                expense.created_by = request.user
                expense.amount = -abs(expense.amount)
                expense.save()
                return redirect('transactions:transaction_list')
        else:
            form = forms.CreateExpense(instance=transaction, user=request.user)

    return render(request, "transaction_edit.html", {'form': form, 'transaction': transaction})

@login_required(login_url="/members/login/")
def transaction_create_expense(request):
    if(request.method == "POST"):
        form = forms.CreateExpense(request.POST, user=request.user)
        if form.is_valid():
            # save
            new_expense = form.save(commit=False)
            new_expense.created_by = request.user
            # expenses always shoud be saved as negative amount transaction
            new_expense.amount = -abs(new_expense.amount)
            new_expense.save()
            return redirect('transactions:transaction_list')
    else:
        form = forms.CreateExpense(initial={'date': timezone.now().date()}, user=request.user)
    return render(request, 'transaction_create_expense.html', {'form': form})

@login_required(login_url="/members/login/")
def transaction_create_income(request):
    if(request.method == "POST"):
        form = forms.CreateIncome(request.POST, user=request.user)
        if form.is_valid():
            # save
            new_income = form.save(commit=False)
            new_income.created_by = request.user
            # income always shoud be saved as positive amount transaction
            new_income.amount = abs(new_income.amount)
            new_income.save()
            return redirect('transactions:transaction_list')
    else:
        form = forms.CreateIncome(initial={'date': timezone.now().date()}, user=request.user)
    return render(request, 'transaction_create_income.html', {'form': form})


@login_required(login_url="/members/login/")
def account_create(request):
    if request.method == "POST":
        form = forms.CreateAccount(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.family = request.user.profile.family
            new_account.save()
            return redirect('transactions:account_list')
    else:
        form = forms.CreateAccount()
    return render(request, 'account_create.html',  {'form': form})

@login_required(login_url="/members/login/")
def account_list(request):
    user = request.user
    accounts_data = Account.objects.filter(family= getattr(user.profile, 'family', None)).order_by('name')
    return render(request, "account_list.html", {"data": accounts_data})

@login_required(login_url="/members/login/")
def account_edit(request, id):
    account = Account.objects.get(id=id)
    if request.POST.get("action") == "delete":
        account.delete()
        return redirect('transactions:account_list')
    
    if request.POST.get("action") == "cansel":
        return redirect('transactions:account_list')
    
    if request.method == "POST":
        form = forms.CreateAccount(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('transactions:account_list')
    
    form = forms.CreateAccount(instance=account)
    return render(request, 'account_edit.html',  {'form': form, 'account': account})



@login_required(login_url="/members/login/")
def currency_list(request):
    user = request.user
    data = Currency.objects.filter(family= getattr(user.profile, 'family', None)).order_by('code')
    return render(request, "currency_list.html", {"data": data})

@login_required(login_url="/members/login/")
def currency_create(request):
    if request.method == "POST":
        form = forms.CreateCurrency(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.family = request.user.profile.family
            new.save()
            return redirect('transactions:currency_list')
    else:
        form = forms.CreateCurrency()
    return render(request, 'currency_create.html',  {'form': form})

@login_required(login_url="/members/login/")
def currency_edit(request, id):
    currency = Currency.objects.get(id=id)
    if request.POST.get("action") == "delete":
        currency.delete()
        return redirect('transactions:currency_list')
    
    if request.POST.get("action") == "cansel":
        return redirect('transactions:currency_list')
    
    if request.method == "POST":
        form = forms.CreateCurrency(request.POST, instance=currency)
        if form.is_valid():
            form.save()
            return redirect('transactions:currency_list')
    
    form = forms.CreateCurrency(instance=currency)
    return render(request, 'currency_edit.html',  {'form': form, 'currency': currency})


@login_required(login_url="/members/login/")
def category_list(request):
    user = request.user
    data = Category.objects.filter(family= getattr(user.profile, 'family', None)).order_by('name')
    return render(request, "category_list.html", {"data": data})

@login_required(login_url="/members/login/")
def category_create(request):
    if request.method == "POST":
        form = forms.CreateCategory(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.family = request.user.profile.family
            new.save()
            return redirect('transactions:category_list')
    else:
        form = forms.CreateCategory()
    return render(request, 'category_create.html',  {'form': form})

@login_required(login_url="/members/login/")
def category_edit(request, id):
    category = Category.objects.get(id=id)
    if request.POST.get("action") == "delete":
        category.delete()
        return redirect('transactions:category_list')
    
    if request.POST.get("action") == "cansel":
        return redirect('transactions:category_list')
    
    if request.method == "POST":
        form = forms.CreateCategory(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('transactions:category_list')
    
    form = forms.CreateCategory(instance=category)
    return render(request, 'category_edit.html',  {'form': form, 'category': category})