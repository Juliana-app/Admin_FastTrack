# sede/views.py
from django.shortcuts import render, redirect
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
    return render(request, 'sede/crear_sede.html', {'form': form})
