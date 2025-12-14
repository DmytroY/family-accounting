from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import loader
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, EditUserForm
import secrets
from django.db.models.deletion import ProtectedError

@login_required(login_url="/accounts/login/")
def list(request):
    """
    render list of user with family field same as current logged user one
    """
    current_family = request.user.profile.family
    mymembers = User.objects.filter(profile__family=current_family)
    return render(request, "all_members.html", {'mymembers':mymembers})

@login_required(login_url="/accounts/login/")
def member_edit(request, uuid):
    try:
        mymember = User.objects.get(profile__uuid=uuid)
        if mymember and mymember.profile.family == request.user.profile.family:
            if request.POST.get("action") == "delete":
                try:
                    mymember.delete()
                    messages.success(request, f"user {mymember.username} deleted.")
                    return redirect("members:list")
                except ProtectedError:
                    messages.error(request, "Can't delete user It is used by existing transaction records.")
                    return redirect("members:member_edit", uuid=uuid)
            
            if request.method == "POST":
                print(f"--DY-- saving user data")
                form = EditUserForm(request.POST, instance=mymember)
                if form.is_valid():
                    print(f"--DY-- form is valid")
                    form.save()
                    messages.success(request, "User data saved")
                    return redirect('members:list')
                else:
                    print(f"--DY-- form errors: {form.errors}")
                    messages.error(request, f"error: {form.errors}")
                    # Re-render with form errors so user can correct them
                    return render(request, 'member_edit.html', {'form': form})

            form = EditUserForm(instance=mymember)
            return render(request, 'member_edit.html',  {'form': form, 'mymember': mymember})

        raise Http404()
    except:
        raise Http404()

@login_required(login_url="/accounts/login/")
def member_create(request):
    family_token = request.user.profile.family
    if request.method == "POST":
        form = RegisterForm(request.POST, family_token=family_token)
        if form.is_valid():
            user = form.save()
            user.profile.family = form.cleaned_data["family"]
            user.profile.save()
            login(request, user)
            return redirect("members:list")
    else:
        form = RegisterForm(family_token=family_token)
    return render(request, "register.html", {"form": form})

def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())

def register_view(request):
    family_token = secrets.token_urlsafe(16)
    if request.method == "POST":
        form = RegisterForm(request.POST, family_token=family_token)
        if form.is_valid():
            user = form.save()
            user.profile.family = form.cleaned_data["family"]
            user.profile.save()
            login(request, user)
            return redirect("members:list")
    else:
        form = RegisterForm(family_token=family_token)
    return render(request, "register.html", {"form": form})

def login_view(request):
    if(request.method == "POST"):
        form = AuthenticationForm(data=request.POST)
        if(form.is_valid()):
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("members:list")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    if(request.method == "POST"):
        logout(request)
        return redirect("members:list")
    
def password_reset(request):
    return render(request, "password_reset.html")