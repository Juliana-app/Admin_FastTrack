from rest_framework import generics
from .models import Producto
from .serializers import ProductoSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect  
from pedidos.models import Pedido

class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoUpdateView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    
@login_required
def dashboard_general(request):
    if request.user.rol not in ['admin', 'cajero']:
        return redirect('dashboard')

    productos = Producto.objects.all().order_by('stock')
    pedidos = Pedido.objects.filter(estado='pendiente').order_by('-creado')[:5]  # últimos 5

    return render(request, 'dashboard_general.html', {
        'productos': productos,
        'pedidos': pedidos
    })
