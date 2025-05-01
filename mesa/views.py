from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from sede.models import Sede
from .models import Mesa
from .forms import MesaForm
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def listar_mesas(request):
    sedes = Sede.objects.all()
    sede_id = request.GET.get('sede')
    ordenar_por = request.GET.get('orden') 

    mesas = Mesa.objects.all()
    
    if sede_id:
        mesas = mesas.filter(sede_id=sede_id)

    if ordenar_por:
        mesas = mesas.order_by(ordenar_por)
    else:
        mesas = mesas.order_by('numeroMesa')  # Orden predeterminado

    return render(request, 'mesa/mesa.html', {
        'mesas': mesas,
        'sedes': sedes,
        'sede_id': sede_id
    })


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
    sedes = Sede.objects.all()
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_mesas')  # Redirige a la vista 'listar_mesas'
    else:
        form = MesaForm()

    mesas = Mesa.objects.all()
    return render(request, 'mesa/mesa.html', {
        'form': form,
        'mesas': mesas,
        'sedes': sedes 
    })

@login_required
def ver_mesas(request):
    sede_id = request.GET.get('sede')
    ordenar_por = request.GET.get('orden')

    mesas = Mesa.objects.select_related('sede').all()

    if sede_id:
        mesas = mesas.filter(sede_id=sede_id)

    if ordenar_por:
        mesas = mesas.order_by(ordenar_por)

    sedes = Sede.objects.all()
    return render(request, 'mesa/mesa.html', {'mesas': mesas, 'sedes': sedes, 'sede_id': sede_id})

@login_required
@user_passes_test(es_admin)
def editar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    sedes = Sede.objects.all()  

    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            return redirect('listar_mesas')
    else:
        form = MesaForm(instance=mesa)

    return render(request, 'mesa/editar_mesa.html', {
        'form': form,
        'sedes': sedes, 
        'mesa': mesa     
    })


@login_required
@user_passes_test(es_admin)
def eliminar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    mesa.delete()
    return redirect('listar_mesas')

@login_required
@user_passes_test(es_admin)
def mesas_registradas_view(request):
    sede_id = request.GET.get('sede')
    orden = request.GET.get('orden')

    mesas = Mesa.objects.all()

    if sede_id:
        mesas = mesas.filter(sede_id=sede_id)

    if orden:
        mesas = mesas.order_by(orden)

    sedes = Sede.objects.all()

    return render(request, 'mesa/mesa.html', {
        'mesas': mesas,
        'sedes': sedes,
        'sede_id': sede_id,
    })