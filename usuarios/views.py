from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from inventario.models import InventarioProducto
from mesa.models import Mesa
from pedidos.models import Pedido
from productos.models import Producto
from sede.models import Sede
from .models import Usuario
from .forms import CrearUsuarioForm, LoginForm

def vista_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirección por rol
            if user.rol == 'mesero':
                return redirect('dashboard_mesero')
            elif user.rol == 'cajero':
                return redirect('dashboard_cajero')
            elif user.rol == 'administrador':
                return redirect('dashboard_admin')
            return redirect('/')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')

    return render(request, 'login.html')

def vista_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    rol = request.user.rol
    if rol == 'mesero':
        return redirect('dashboard_mesero')
    elif rol == 'cajero':
        return redirect('dashboard_cajero')
    elif rol == 'administrador':
        return redirect('dashboard_admin')
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
    elif rol == 'administrador':
        return redirect('dashboard_admin')
    return redirect('login')

@login_required
def crear_usuario(request):
    if request.user.rol != 'administrador':
        return redirect('dashboard')

    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('listar_usuarios')
    else:
        form = CrearUsuarioForm()

    return render(request, 'usuarios/crear_usuario.html', {'form': form})

@login_required
def listar_usuarios(request):
    if request.user.rol != 'administrador':
        return redirect('dashboard')

    sedes = Sede.objects.all()
    query = request.GET.get('q')
    sede_id = request.GET.get('sede')

    usuarios = Usuario.objects.select_related('sede').all()

    if query:
        usuarios = usuarios.filter(Q(username__icontains=query) | Q(email__icontains=query))

    if sede_id:
        usuarios = usuarios.filter(sede__id=sede_id)

    return render(request, 'usuarios/listar_usuarios.html', {
        'usuarios': usuarios.order_by('username'),
        'sedes': sedes,
        'query': query,
        'sede_id': sede_id,
    })

@login_required
def editar_usuario(request, usuario_id):
    if request.user.rol != 'administrador':
        return redirect('dashboard')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('rol')
        sede_id = request.POST.get('sede')

        usuario.username = username
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.email = email
        usuario.rol = rol
        usuario.sede_id = sede_id

        if password:  # Solo actualiza si se ingresó
            usuario.set_password(password)

        usuario.save()
        messages.success(request, "Usuario actualizado exitosamente.")
        return redirect('listar_usuarios')

    return redirect('listar_usuarios')

@login_required
def eliminar_usuario(request, usuario_id):
    if request.user.rol != 'administrador':
        return redirect('dashboard')

    usuario = Usuario.objects.get(id=usuario_id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('listar_usuarios')

@login_required
def panel_general(request):
    sede = request.user.sede

    mesas = Mesa.objects.filter(sede=sede)
    
    mesas_vacias_count = mesas.filter(ocupada=False).count()
    mesas_ocupadas_count = mesas.filter(ocupada=True).count()
    
    pedidos_pendientes_count = Pedido.objects.filter(estado='pendiente', mesa__sede=sede).count()
    pedidos_pagados_count = Pedido.objects.filter(estado='pagado', mesa__sede=sede).count()
    
    productos = InventarioProducto.objects.select_related('producto') \
                                          .filter(sede=sede) \
                                          .order_by('cantidad')

    print("Productos en inventario para la sede:", productos)

    return render(request, 'general.html', {
        'mesas': mesas,
        'mesas_vacias_count': mesas_vacias_count,
        'mesas_ocupadas_count': mesas_ocupadas_count,
        'pedidos_pendientes_count': pedidos_pendientes_count,
        'pedidos_pagados_count': pedidos_pagados_count,
        'productos': productos,
    })

