from django.shortcuts import render
from django.utils.translation import gettext as _, activate

def home(request):
    return render(request, "home.html")

def test(request):
    # activate('es')  # force Spanish for testing
    context = {'hello': _("Hello")}
    return render(request, "test.html", context)
