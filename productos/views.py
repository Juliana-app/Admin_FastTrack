from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm

def crear_producto_general(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_producto')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form, 'productos': productos})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm

def editar_producto_general(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/editar_producto.html', {
        'form': form,
        'producto': producto
    })

def eliminar_producto_general(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('crear_producto')
