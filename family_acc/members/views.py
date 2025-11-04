from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Member
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def list(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template("all_members.html")
    context ={'mymembers':mymembers, }
    return HttpResponse(template.render(context, request))

def details(request, slug):
    mymember = Member.objects.get(slug=slug)
    template = loader.get_template("details.html")
    context ={'mymember':mymember, }
    return HttpResponse(template.render(context, request))

def testing(request):
    return render(request, "test_template.html")

def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())

def register_view(request):
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            # form.save()
            login(request, form.save())
            return redirect("members:list")
    else:
        form = UserCreationForm() 
    return render(request, "register.html", {"form": form})

def login_view(request):
    if(request.method == "POST"):
        form = AuthenticationForm(data=request.POST)
        if(form.is_valid()):
            login(request, form.get_user())
            print("--DY-- successfull login")
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("transactions:list")
        print("--DY-- login problem")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    if(request.method == "POST"):
        logout(request)
        return redirect("members:list")
    
    
