from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
# from .models import Member
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

@login_required(login_url="/members/login/")
def list(request):
    current_family = request.user.profile.family
    mymembers = User.objects.filter(profile__family=current_family)
    return render(request, "all_members.html", {'mymembers':mymembers})

@login_required(login_url="/members/login/")
def details(request, id):
    print(f"--DY-- views.py:details  id = {id}")
    mymember = User.objects.get(id=id)
    template = loader.get_template("details.html")
    context ={'mymember':mymember, }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.family = form.cleaned_data["family"]
            user.profile.save()
            login(request, user)
            return redirect("members:list")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


    # if(request.method == "POST"):
    #     form = UserCreationForm(request.POST)
    #     if(form.is_valid()):
    #         # form.save()
    #         login(request, form.save())
    #         return redirect("members:list")
    # else:
    #     form = UserCreationForm() 
    # return render(request, "register.html", {"form": form})

def login_view(request):
    if(request.method == "POST"):
        form = AuthenticationForm(data=request.POST)
        if(form.is_valid()):
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("transactions:list")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    if(request.method == "POST"):
        logout(request)
        return redirect("members:list")
    
    
