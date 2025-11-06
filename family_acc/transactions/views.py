from django.shortcuts import render, redirect
from .models import Transaction
from django.contrib.auth.decorators import login_required
from . import forms
from django.utils import timezone


@login_required(login_url="/members/login/")
def list(request):
    user = request.user
    attr = getattr(user.profile, 'family', None)
    if(getattr(user.profile, 'family', None) == "test"):
        transaction_data = Transaction.objects.order_by('-date')[:5]
    else:
        transaction_data = Transaction.objects.order_by('-date')[:3]
    return render(request, "list.html", {"data": transaction_data})

@login_required(login_url="/members/login/")
def create_expence(request):
    if(request.method == "POST"):
        form = forms.CreateExpence(request.POST)
        if form.is_valid():
            # save
            new_expence = form.save(commit=False)
            new_expence.created_by = request.user
            new_expence.save()
            return redirect('transactions:list')
    else:
        form = forms.CreateExpence(initial={'date': timezone.now().date()})
    return render(request, 'create_expence.html', {'form': form})
