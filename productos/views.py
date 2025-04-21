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

def editar_producto_general(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductoForm(instance=producto)
        return JsonResponse({
            'id': producto.id,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion
        })

def eliminar_producto_general(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('lista_productos')
