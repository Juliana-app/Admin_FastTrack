from django.shortcuts import render, redirect

from inventario.models import InventarioProducto
from django.contrib.auth.decorators import login_required
from .forms import PrecioForm
from .models import HistorialPrecio

@login_required
def registrar_precio(request):
    if request.method == 'POST':
        form = PrecioForm(request.POST)
        if form.is_valid():
            historial = form.save()
            
            # Actualizar el precio_venta en InventarioProducto para todas las sedes
            inventarios = InventarioProducto.objects.filter(producto=historial.producto)
            for inventario in inventarios:
                inventario.precio_venta = historial.precio_venta
                inventario.save()

            return redirect('registrar_precio')
    else:
        form = PrecioForm()

    historial = HistorialPrecio.objects.select_related('producto').order_by('-fecha')[:20]
    return render(request, 'historial/registrar_precio.html', {
        'form': form,
        'historial': historial
    })
