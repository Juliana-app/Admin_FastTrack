# sede/views.py
from django.shortcuts import get_object_or_404, render, redirect
from .models import Sede
from .forms import SedeForm

def crear_sede(request):
    if request.method == 'POST':
        form = SedeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_sedes')  # Redirigir a una lista o a donde prefieras
    else:
        form = SedeForm()
    return render(request, 'sedes/crear_sede.html', {'form': form})

def listar_sedes(request):
    sedes = Sede.objects.all()
    return render(request, 'sedes/listar_sedes.html', {'sedes': sedes})

def editar_sede(request, sede_id):
    sede = Sede.objects.get(pk=sede_id)
    if request.method == 'POST':
        form = SedeForm(request.POST, instance=sede)
        if form.is_valid():
            form.save()
            return redirect('listar_sedes')
    else:
        form = SedeForm(instance=sede)
    return render(request, 'sedes/editar_sede.html', {'form': form, 'sede': sede})

def eliminar_sede(request, sede_id):
    sede = get_object_or_404(Sede, id=sede_id)
    sede.delete()
    return redirect('listar_sedes')
