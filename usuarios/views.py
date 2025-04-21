from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Usuario
from .forms import RegistroForm, LoginForm
from django.contrib import messages

from django.http import HttpResponse

def vista_login(request):
    print("Método:", request.method)  
    if request.method == 'POST':
        print("Entró al POST")

        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Usuario:", username)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("Autenticado:", user.username, "Rol:", user.rol)
            login(request, user)

            # Redirección automática según rol
            if user.rol == 'mesero':
                return redirect('dashboard_mesero')
            elif user.rol == 'cajero':
                return redirect('dashboard_cajero')
            elif user.rol == 'administrador':
                return redirect('dashboard_admin') 

            return redirect('/')  # Redirección de respaldo si no matchea rol

        else:
            print("Falló la autenticación")
            messages.error(request, 'Usuario o contraseña inválidos.')

    return render(request, 'login.html')


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
    return render(request, 'usuarios/dashboard_mesero.html')

@login_required
def dashboard_cajero(request):
    return render(request, 'usuarios/caja_dashboard.html')

@login_required
def dashboard_admin(request):
    return render(request, 'usuarios/dashboard_admin.html')

@login_required
def redireccion_por_rol(request):
    rol = request.user.rol
    if rol == 'mesero':
        return redirect('dashboard_mesero')
    elif rol == 'cajero':
        return redirect('dashboard_cajero')
    elif rol == 'admin':
        return redirect('dashboard_admin')
    else:
        return redirect('login')