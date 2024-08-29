from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['dni', 'numer_phone', 'first_name', 'last_name', 'email', 'password1', 'password2']