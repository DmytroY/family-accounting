from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Member
# from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

import json

def testing(request):
    return redirect("main")
    
    print(request.method)
    print(request.path)
    print(request.GET)
    print(request.headers)
    # print(request.META)
    return HttpResponse("Hello world!")
    # template = loader.get_template("test_template.html")
    # mydata = Member.objects.order_by('-firstname', 'phone')
    # context = {'members': mydata,}
    # return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())

def register(request):
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect("main")
    else:
        form = UserCreationForm() 
    return render(request, "register.html", {"form": form})

def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template("all_members.html")
    context ={'mymembers':mymembers, }
    return HttpResponse(template.render(context, request))

def details(request, slug):
    mymember = Member.objects.get(slug=slug)
    template = loader.get_template("details.html")
    context ={'mymember':mymember, }
    return HttpResponse(template.render(context, request))
