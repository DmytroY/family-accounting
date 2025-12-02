from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    family = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ["username", "family", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        token = kwargs.pop("family_token", None)
        super().__init__(*args, **kwargs)
        if token:
            self.fields["family"].initial = token