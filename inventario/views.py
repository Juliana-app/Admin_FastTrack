from pyexpat.errors import messages
from rest_framework import generics
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
    productos = InventarioProducto.objects.select_related('producto', 'sede').order_by('producto__nombre')
    form = ProductoInventarioForm()
    return render(request, 'productos/lista_productos.html', {
        'productos': productos,
        'form': form,
    })

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.cantidad = int(request.POST.get('cantidad'))
        producto.stock_minimo = int(request.POST.get('stock_minimo'))
        producto.save()
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('productos/lista_productos')

    return render(request, 'productos/editar_producto.html', {'producto': producto})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.delete()
    messages.warning(request, 'Producto eliminado.')
    return redirect('productos/lista_productos')


@require_POST
@login_required
def crear_producto_inventario(request):
    form = ProductoInventarioForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('lista_productos')
