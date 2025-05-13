from pyexpat.errors import messages
from rest_framework import generics

from historial.models import HistorialPrecio
from .models import Producto, InventarioProducto
from .serializers import ProductoSerializer
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect  
from pedidos.models import Pedido
from .forms import ProductoInventarioForm

class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoUpdateView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    
@login_required
def dashboard_general(request):
    if request.user.rol not in ['admin', 'cajero']:
        return redirect('dashboard')

    productos = Producto.objects.all().order_by('cantidad')
    pedidos = Pedido.objects.filter(estado='pendiente').order_by('-creado')[:5]  # últimos 5

    return render(request, 'usuarios/dashboard_general.html', {
        'productos': productos,
        'pedidos': pedidos
    })
    

@login_required
def lista_productos(request):
    if request.user.rol not in ['administrador', 'cajero']:
        return redirect('dashboard')

    sede_usuario = request.user.sede
    productos = InventarioProducto.objects.select_related('producto', 'sede') \
                                          .filter(sede=sede_usuario) \
                                          .order_by('producto__nombre')

    form = ProductoInventarioForm()
    return render(request, 'productos/lista_productos.html', {
        'productos': productos,
        'form': form,
    })

@login_required
def editar_producto_modal(request, pk):
    producto = get_object_or_404(InventarioProducto, pk=pk)
    if request.method == 'POST':
        form = ProductoInventarioForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # o la vista principal del inventario
    return redirect('productos/lista_productos')

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.delete()
    messages.warning(request, 'Producto eliminado.')
    return redirect('productos/lista_productos')


@require_POST
@login_required
def crear_producto_inventario(request):
    form = ProductoInventarioForm(request.POST, request.FILES)
    if form.is_valid():
        inventario = form.save(commit=False)

        # Asignar la sede automáticamente desde el usuario
        inventario.sede = request.user.sede

        # Asignar el precio desde el historial
        ultimo_precio = HistorialPrecio.objects.filter(producto=inventario.producto).order_by('-fecha').first()
        if ultimo_precio:
            inventario.precio_venta = ultimo_precio.precio_venta

        inventario.save()
    else:
        print("Errores:", form.errors)  # Debug
    return redirect('lista_productos')
