# productos/views.py
from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm

def crear_producto_general(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_producto')  # Redirige a la misma vista
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form, 'productos': productos})
