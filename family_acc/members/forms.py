from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    """Form for registering new user (handles password validation and hashing automatically)"""
    family = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name","email", "username", "password1", "password2","family"]

    def __init__(self, *args, **kwargs):
        token = kwargs.pop("family_token", None)
        super().__init__(*args, **kwargs)
        # self registration will generate family token
        # registration by other existing user will extend existing family token
        if token:
            self.fields["family"].initial = token

        # username and password are required by default
        # add othe filds as required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


class EditUserForm(forms.ModelForm):
    """Form for editing existing user (no password required)"""

    class Meta:
        model = User
        fields = ["first_name", "last_name","email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # required filds
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
