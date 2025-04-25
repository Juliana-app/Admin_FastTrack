from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Mesa
from .forms import MesaForm
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def listar_mesas(request):
    # Solo mesas de la sede del usuario
    mesas = Mesa.objects.filter(sede=request.user.sede)
    return render(request, 'mesas.html', {'mesas': mesas})

@require_POST
@login_required
def ocupar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id, sede=request.user.sede)
    if not mesa.ocupada:
        mesa.ocupada = True
        mesa.save()
    return redirect('listar_mesas')

@require_POST
@login_required
def liberar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id, sede=request.user.sede)
    if mesa.ocupada:
        mesa.ocupada = False
        mesa.save()
    return redirect('listar_mesas')

def es_admin(user):
    return user.is_authenticated and user.rol == 'administrador'

@login_required
@user_passes_test(es_admin)
def crear_mesa(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_admin')
    else:
        form = MesaForm()
    return render(request, 'mesa/crear_mesa.html', {'form': form})

def ver_mesas(request):
    mesas = Mesa.objects.select_related('sede').all()
    return render(request, 'mesa/mesa.html', {'mesas': mesas})

@login_required
@user_passes_test(es_admin)
def editar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            return redirect('ver_mesas')
    else:
        form = MesaForm(instance=mesa)
    return render(request, 'mesa/editar_mesa.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def eliminar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    mesa.delete()
    return redirect('ver_mesas')
