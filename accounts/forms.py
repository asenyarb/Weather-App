from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label=(""), max_length=10, widget=forms.TextInput(attrs=({
        'class': "form-control mt-md-5",
        'name': "username",
        'id': "id_username",
        'placeholder': "Username",
        'required': True,
    })))
    first_name = forms.CharField(label=(""), max_length=10, widget=forms.TextInput(attrs=({
        'class': "form-control mt-4",
        'name': "first_name",
        'id': "id_first_name",
        'placeholder': "First name",
        'required': False,
    })))
    last_name = forms.CharField(label=(""), max_length=10, widget=forms.TextInput(attrs=({
        'class': "form-control mt-4",
        'name': "last_name",
        'id': "id_last_name",
        'placeholder': "Last name",
        'required': False,
    })))
    email = forms.EmailField(label=(""), widget=forms.EmailInput(attrs=({
        'class': "form-control mt-4",
        'name': "email",
        'id': "id_email",
        'placeholder': "Email",
        'required': True,
    })))
    password1 = forms.CharField(label=(""), widget=forms.PasswordInput(attrs=({
        'class': "form-control mt-4",
        'name': "password1",
        'id': "id_password1",
        'placeholder': "Password",
        'required': True,
    })))
    password2 = forms.CharField(label=(""), widget=forms.PasswordInput(attrs=({
        'class': "form-control mt-4",
        'name': "password2",
        'id': "id_password2",
        'placeholder': "Password confirmation",
        'required': True,
    })))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LogInForm(AuthenticationForm):
    username = forms.CharField(label=(""), max_length=254, widget=forms.TextInput(attrs={
                'class': "form-control mt-md-5",
                'name': "username",
                'id': "id_username",
                'placeholder': "username",
                'autofocus': True,
                'required': True,
            }))
    password = forms.CharField(label=(""), widget=forms.PasswordInput(attrs={
                'class': "form-control mt-4",
                'name': "password",
                'id': "id_password",
                'placeholder': "password",
                'required': True,
            }))
