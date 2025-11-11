from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    family = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["username", "family", "email", "password1", "password2"]