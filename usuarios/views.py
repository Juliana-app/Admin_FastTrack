from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Usuario
from .forms import RegistroForm, LoginForm

def vista_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if usuario:
                login(request, usuario)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def vista_logout(request):
    logout(request)
    return redirect('login')

def vista_registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def dashboard(request):
    rol = request.user.rol
    if rol == 'mesero':
        return redirect('dashboard_mesero')
    elif rol == 'cajero':
        return redirect('dashboard_cajero')
    elif rol == 'admin':
        return redirect('dashboard_admin')
    else:
        return redirect('login')

@login_required
def dashboard_mesero(request):
    return render(request, 'dashboard_mesero.html')

@login_required
def dashboard_cajero(request):
    return render(request, 'dashboard_cajero.html')

@login_required
def dashboard_admin(request):
    return render(request, 'dashboard_admin.html')
