
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.views.decorators.csrf import csrf_protect

def home(request):
    return render(request, 'home.html')

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():  # Verifica si los datos son válidos
            email = form.cleaned_data.get('username')  # Aunque se llama 'username', es un email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)  # Autentica al usuario
            if user is not None:
                login(request, user)  # Inicia sesión al usuario
                return redirect('profile')  # Redirige al perfil o cualquier otra vista
            else:
                messages.error(request, "Credenciales incorrectas.")
        else:
            messages.error(request, "Datos inválidos.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('home')
 