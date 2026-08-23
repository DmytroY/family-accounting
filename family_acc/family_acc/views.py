from django.shortcuts import render


def home(request):
    return render(request, "home.html")

def test(request):

    context = {'hello': _("Hello")}
    return render(request, "test.html", context)