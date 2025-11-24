from django.shortcuts import render, redirect
from .models import Transaction, Account, Currency, Category
from django.contrib.auth.decorators import login_required
from . import forms
from django.utils import timezone
from django.db.models import F
from django.http import JsonResponse
from django.db.models.deletion import ProtectedError
from django.contrib import messages


@login_required(login_url="/members/login/")
def get_account_currency(request, account_id):
    """ helper function used in get_currency.js"""
    account = Account.objects.get(id=account_id)
    return JsonResponse({"currency": account.currency.code})

@login_required(login_url="/members/login/")
def transaction_list(request):
    user = request.user
    family = getattr(user.profile, 'family', None)

    # get date range from GET params
    start = request.GET.get("start")
    end = request.GET.get("end")

    # default = current month
    today = timezone.now().date()
    cur_month_start = today.replace(day=1)

    if start and end:
        transaction_data = Transaction.objects.filter(
            family=family,
            date__range=[start, end]
        ).order_by('-date', '-id')
        print(f"--DY-- start:{start}")
    else:
        transaction_data = Transaction.objects.filter(
            family=family,
            date__gte=cur_month_start
        ).order_by('-date', '-id')

    return render(request, "transaction_list.html", {"data": transaction_data})

@login_required(login_url="/members/login/")
def transaction_edit(request, id):
    transaction = Transaction.objects.get(id=id)

    # POST
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete":
            # adjust account balance
            Account.objects.filter(id=transaction.account_id).update(balance=F('balance') - transaction.amount)
            #delete transaction
            transaction.delete()
            messages.success(request, f"Transaction deleted.")
            return redirect('transactions:transaction_list')
        
        if action == "cancel":
            return redirect('transactions:transaction_list')
        
        if action == "save":
            amt_old = transaction.amount
            if transaction.amount >= 0:         
                # treat it as income
                form = forms.CreateIncome(request.POST, instance=transaction, user=request.user)
                sign = 1
            else:
                #treat as expence
                form = forms.CreateExpense(request.POST, instance=transaction, user=request.user)
                sign = -1
            
            if form.is_valid():
                tr = form.save(commit=False)
                tr.amount = sign * abs(tr.amount)
                tr.created_by = request.user
                # adjust account balance
                Account.objects.filter(id=transaction.account_id).update(balance=F('balance') + (tr.amount - amt_old))
           
                tr.save()
                messages.success(request, f"Transaction edited.")
                return redirect('transactions:transaction_list')
            
    # GET
    if transaction.amount >= 0:
        form = forms.CreateIncome(instance=transaction, user=request.user)
    else:
        form = forms.CreateExpense(instance=transaction, user=request.user)
    return render(request, "transaction_edit.html", {'form': form, 'transaction': transaction})

@login_required(login_url="/members/login/")
def transaction_create_expense(request):
    if(request.method == "POST"):
        form = forms.CreateExpense(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            # expenses always shoud be saved as negative amount transaction
            expense.amount = -abs(expense.amount)
            expense.currency = Currency.objects.get(id=expense.account.currency_id)
            # adjust acount balance accordingly
            Account.objects.filter(id=expense.account_id).update(balance=F('balance') + expense.amount)
            #commit changes
            expense.save()
            messages.success(request, "Expence transaction created")
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
            income = form.save(commit=False)
            income.created_by = request.user
            # income always shoud be saved as positive amount transaction
            income.amount = abs(income.amount)
            income.currency = Currency.objects.get(id=income.account.currency_id)
            # adjust acount balance accordingly
            Account.objects.filter(id=income.account_id).update(balance=F('balance') + income.amount)
            income.save()
            messages.success(request, "Income transaction created")
            return redirect('transactions:transaction_list')
    else:
        form = forms.CreateIncome(initial={'date': timezone.now().date()}, user=request.user)
    return render(request, 'transaction_create_income.html', {'form': form})


@login_required(login_url="/members/login/")
def account_create(request):
    if request.method == "POST":
        form = forms.CreateAccount(request.POST, user=request.user)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.family = request.user.profile.family
            new_account.save()
            messages.success(request, f"Account {new_account.name} created")
            return redirect('transactions:account_list')
        else:
            messages.error(request, "Cannot create account. Account with such name and currency already exists")
            return render(request, 'account_create.html',  {'form': form})
    else:
        form = forms.CreateAccount(user=request.user)
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
        try:
            account.delete()
            messages.success(request, f"Account {account.name} deleted.")

            return redirect('transactions:account_list')
        except ProtectedError:
            messages.error(request, 'Cannot delete account. It is used by existing transaction records.')
            return redirect('transactions:account_edit',  id=id)
    
    if request.POST.get("action") == "cansel":
        return redirect('transactions:account_list')
    
    if request.method == "POST":
        form = forms.CreateAccount(request.POST, instance=account, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('transactions:account_list')
    
    form = forms.CreateAccount(instance=account, user=request.user)
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
            messages.success(request, f"New currency {new.code} created")
            return redirect('transactions:currency_list')
    else:
        form = forms.CreateCurrency()
    return render(request, 'currency_create.html',  {'form': form})

@login_required(login_url="/members/login/")
def currency_edit(request, id):
    currency = Currency.objects.get(id=id)

    if request.POST.get("action") == "delete":
        try:
            currency.delete()
            messages.success(request, f"Currency {currency.code} deleted.")
            return redirect('transactions:currency_list')
        except ProtectedError:
            messages.error(request, "Cannot delete. Currency is used in existing transactions.")
            return redirect('transactions:currency_edit', id=id)
            
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
            messages.success(request, f"New categoty {new.name} created")
            return redirect('transactions:category_list')
    else:
        form = forms.CreateCategory()
    return render(request, 'category_create.html',  {'form': form})

@login_required(login_url="/members/login/")
def category_edit(request, id):
    category = Category.objects.get(id=id)

    if request.POST.get("action") == "delete":
        try:
            category.delete()
            messages.success(request, f"Category {category.name} deleted.")
            return redirect('transactions:category_list')
        except ProtectedError:
            messages.error(request, "Cannot delete. Category is used in existing transactions.")
            return redirect('transactions:category_edit', id=id)
    
    if request.POST.get("action") == "cansel":
        return redirect('transactions:category_list')
    
    if request.method == "POST":
        form = forms.CreateCategory(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('transactions:category_list')
    
    form = forms.CreateCategory(instance=category)
    return render(request, 'category_edit.html',  {'form': form, 'category': category})