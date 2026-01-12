from django.shortcuts import render
from django.utils.translation import gettext as _

def home(request):
    return render(request, "home.html")

def test(request):

    context = {'hello': _("Hello")}
    return render(request, "test.html", context)
