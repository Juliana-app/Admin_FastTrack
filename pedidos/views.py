import csv
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from mesa.models import Mesa
from .models import Pedido, PedidoProducto
from .serializers import PedidoSerializer
from inventario.models import InventarioProducto, Producto


class PedidoListCreateView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all().order_by('-creado')
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]


class PedidoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]


@login_required
def tomar_pedido(request):
    if request.user.rol not in ['mesero', 'administrador']:
        return redirect('dashboard')

    sede = request.user.sede

    if request.method == 'POST':
        mesa_id = request.POST.get('mesa_id')
        productos = []

        for key, value in request.POST.items():
            if key.startswith('producto_id_'):
                index = key.split('_')[-1]
                cantidad = request.POST.get(f'cantidad_{index}', 0)
                try:
                    nombre_producto = value
                    cantidad = int(cantidad)
                    if cantidad > 0:
                        productos.append((nombre_producto, cantidad))
                except ValueError:
                    continue

        if not productos or not mesa_id:
            messages.error(request, "Debes seleccionar una mesa y al menos un producto.")
            return redirect('tomar_pedido')

        try:
            mesa = Mesa.objects.get(id=mesa_id, sede=sede)
        except Mesa.DoesNotExist:
            messages.error(request, "La mesa seleccionada no es válida.")
            return redirect('tomar_pedido')
        
        mesa = Mesa.objects.get(id=mesa_id, sede=sede)
        mesa.ocupada = True
        mesa.save()


        pedido = Pedido.objects.create(
            usuario=request.user,
            mesa=mesa,
            estado='pendiente',
            creado=datetime.now()
        )

        for nombre_producto, cantidad in productos:
            try:
                producto = Producto.objects.get(nombre=nombre_producto)
                inventario = InventarioProducto.objects.get(producto=producto, sede=sede)
                if inventario.cantidad >= cantidad:
                    PedidoProducto.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=inventario.precio_venta
                    )
                    inventario.cantidad -= cantidad
                    inventario.save()
                else:
                    messages.warning(request, f"Producto {producto.nombre} no tiene stock suficiente.")
            except (Producto.DoesNotExist, InventarioProducto.DoesNotExist):
                messages.warning(request, f"Producto {nombre_producto} no disponible en esta sede.")

        messages.success(request, "Pedido creado correctamente.")
        return redirect('tomar_pedido')

    productos_disponibles = InventarioProducto.objects.filter(
        sede=sede,
        cantidad__gt=0
    ).select_related('producto')

    mesas_disponibles = Mesa.objects.filter(sede=sede)

    return render(request, 'pedidos/tomar_pedido.html', {
        'productos': productos_disponibles,
        'mesas': mesas_disponibles
    })


@login_required
def ver_pedidos(request):
    if request.user.rol not in ['cajero', 'administrador', 'mesero']:
        return redirect('dashboard')

    sede_usuario = request.user.sede

    pedidos = Pedido.objects.filter(
        usuario__sede=sede_usuario,
        estado='pendiente'
    ).select_related('usuario').prefetch_related('productos__producto').order_by('-creado')

    return render(request, 'pedidos/ver_pedidos.html', {'pedidos': pedidos})


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
        writer.writerow([
            pedido.id,
            pedido.usuario.username,
            pedido.mesa.nombre if pedido.mesa else "Sin mesa",
            pedido.estado,
            pedido.creado.strftime('%Y-%m-%d %H:%M'),
            productos
        ])

    return response

@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.user.rol != 'mesero' or pedido.usuario != request.user or pedido.estado != 'pendiente':
        return redirect('ver_pedidos')

    sede = request.user.sede
    inventario = InventarioProducto.objects.filter(sede=sede).select_related('producto')

    if request.method == 'POST':
        nuevos_productos = request.POST.getlist('producto')
        nuevas_cantidades = request.POST.getlist('cantidad')

        for prod_id, cant in zip(nuevos_productos, nuevas_cantidades):
            try:
                cantidad = int(cant)
                producto = Producto.objects.get(id=prod_id)
                invent = InventarioProducto.objects.get(producto=producto, sede=sede)

                if cantidad > 0 and invent.cantidad >= cantidad:
                    PedidoProducto.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=invent.precio_venta  # <-- ASIGNA PRECIO
                    )
                    invent.cantidad -= cantidad  # <-- DESCUENTA STOCK
                    invent.save()
                else:
                    messages.warning(request, f"No hay suficiente stock de {producto.nombre}.")
            except (ValueError, Producto.DoesNotExist, InventarioProducto.DoesNotExist):
                continue

        messages.success(request, "Pedido actualizado.")
        return redirect('ver_pedidos')

    return render(request, 'pedidos/editar_pedido.html', {
        'pedido': pedido,
        'inventario': inventario,
    })

@login_required
def pedidos_por_pagar(request):
    if request.user.rol not in ['cajero', 'administrador']:
        return redirect('dashboard')

    sede_usuario = request.user.sede

    pedidos = Pedido.objects.filter(
        usuario__sede=sede_usuario,
        estado='pendiente'
    ).select_related('usuario').order_by('-creado')

    return render(request, 'pedidos/pedidos_por_pagar.html', {'pedidos': pedidos})


@login_required
def marcar_pedido_pagado(request, pedido_id):
    if request.user.rol not in ['cajero', 'admin']:
        return redirect('dashboard')

    try:
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.marcar_pagado() 

        # Liberar mesa
        mesa = pedido.mesa
        mesa.ocupada = False
        mesa.save()

        messages.success(request, "Pedido marcado como pagado y mesa liberada.")

    except Pedido.DoesNotExist:
        messages.error(request, "El pedido no existe.")

    return redirect('pedidos_por_pagar')


@login_required
def vista_cajero(request):
    if request.user.rol not in ['cajero', 'admin']:
        return redirect('dashboard')
    
    sede = request.user.sede
    pedidos = Pedido.objects.filter(
        usuario__sede=sede,
        estado='pendiente'
    ).order_by('-creado')

    return render(request, 'usuarios/caja_dashboard.html', {
        'pedidos': pedidos,
    })
