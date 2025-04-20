from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .models import Pedido, PedidoProducto
from .serializers import PedidoSerializer
from rest_framework.permissions import IsAuthenticated
from inventario.models import Producto
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from django.utils.dateparse import parse_date

class PedidoListCreateView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all().order_by('-fecha_creacion')
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

class PedidoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

@login_required
def tomar_pedido(request):
    if request.user.rol != 'mesero' and request.user.rol != 'admin':
        return redirect('dashboard')

    if request.method == 'POST':
        mesa = request.POST.get('mesa')
        productos = []

        for key, value in request.POST.items():
            if key.startswith('producto_id_'):
                index = key.split('_')[-1]
                try:
                    prod_id = int(value)
                    cantidad = int(request.POST.get(f'cantidad_{index}', 0))
                    if cantidad > 0:
                        productos.append((prod_id, cantidad))
                except ValueError:
                    continue

        if not productos:
            messages.error(request, "Debe agregar al menos un producto con cantidad válida.")
            return redirect('tomar_pedido')

        pedido = Pedido.objects.create(
            usuario=request.user,
            mesa=mesa,
            estado='pendiente',
            creado=datetime.now()
        )

        for prod_id, cantidad in productos:
            try:
                producto = Producto.objects.get(id=prod_id)
                if producto.stock >= cantidad:
                    PedidoProducto.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad
                    )
                    producto.stock -= cantidad
                    producto.save()
                else:
                    messages.warning(request, f"Producto {producto.nombre} no tiene stock suficiente.")
            except Producto.DoesNotExist:
                messages.warning(request, f"Producto con ID {prod_id} no existe.")

        messages.success(request, "Pedido registrado exitosamente.")
        return redirect('dashboard_mesero')

    return render(request, 'tomar_pedido.html')

@login_required
def ver_pedidos(request):
    if request.user.rol not in ['cajero', 'admin', 'mesero']:
        return redirect('dashboard')

    pedidos = Pedido.objects.filter(estado='pendiente').order_by('-creado')
    return render(request, 'ver_pedidos.html', {'pedidos': pedidos})

@login_required
def marcar_pagado(request, pedido_id):
    if request.user.rol not in ['cajero', 'admin']:
        return redirect('dashboard')

    try:
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.estado = 'pagado'
        pedido.save()
        messages.success(request, "Pedido marcado como pagado.")
    except Pedido.DoesNotExist:
        messages.error(request, "El pedido no existe.")

    return redirect('ver_pedidos')

@login_required
def exportar_csv_pedidos(request):
    if request.user.rol not in ['cajero', 'admin']:
        return redirect('dashboard')

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    pedidos = Pedido.objects.all()
    if fecha_inicio and fecha_fin:
        pedidos = pedidos.filter(
            creado__date__gte=parse_date(fecha_inicio),
            creado__date__lte=parse_date(fecha_fin)
        )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Usuario', 'Mesa', 'Estado', 'Fecha', 'Productos'])

    for pedido in pedidos:
        productos = ", ".join(
            [f"{pp.producto.nombre} ({pp.cantidad})" for pp in pedido.productos.all()]
        )
        writer.writerow([pedido.id, pedido.usuario.username, pedido.mesa, pedido.estado, pedido.creado, productos])

    return response
