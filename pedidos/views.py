import csv
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from historial.models import HistorialPrecio
from mesa.models import Mesa
from .models import Pedido, PedidoProducto
from .serializers import PedidoSerializer
from inventario.models import InventarioProducto, Producto


# API views
class PedidoListCreateView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all().order_by('-creado')
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]


class PedidoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

@login_required
def ver_pedidos(request):
    sede_usuario = request.user.sede

    # Filtro de estado de los pedidos
    estado = request.GET.get('estado', 'todos')

    if estado == 'todos':
        pedidos = Pedido.objects.filter(mesa__sede=sede_usuario)
    elif estado == 'pendiente':
        pedidos = Pedido.objects.filter(mesa__sede=sede_usuario, estado='pendiente')
    else:  # estado == 'pagado'
        pedidos = Pedido.objects.filter(mesa__sede=sede_usuario, estado='pagado')

    if request.method == 'POST':
        mesa_id = request.POST.get('mesa_id')
        productos = request.POST.getlist('producto[]')
        cantidades = request.POST.getlist('cantidad[]')

        if not mesa_id or not productos or not cantidades or len(productos) != len(cantidades):
            messages.error(request, 'Error: Debes seleccionar al menos un producto con su cantidad.')
        else:
            mesa = get_object_or_404(Mesa, id=mesa_id)
            
            # Verificar si la mesa ya está ocupada
            if mesa.ocupada:
                messages.error(request, f'La mesa {mesa.numeroMesa} ya está ocupada. Selecciona otra mesa.')
                return redirect('ver_pedidos')
                
            productos_validos = []

            for producto_id, cantidad in zip(productos, cantidades):
                try:
                    cantidad = int(cantidad)
                    if cantidad <= 0:
                        continue

                    producto = Producto.objects.get(id=producto_id)
                    inventario = InventarioProducto.objects.filter(
                        producto=producto, 
                        sede=sede_usuario
                    ).first()

                    if not inventario:
                        messages.error(request, f"El producto {producto.nombre} no está disponible en tu sede.")
                        continue

                    if cantidad > inventario.cantidad:
                        messages.warning(request, f"No hay suficiente stock de {producto.nombre}.")
                        continue

                    productos_validos.append({
                        'producto': producto,
                        'inventario': inventario,
                        'cantidad': cantidad,
                        'precio': inventario.precio_venta
                    })

                except (ValueError, Producto.DoesNotExist) as e:
                    messages.error(request, f"Error con el producto ID {producto_id}: {str(e)}")
                    continue

            if productos_validos:
                # Marcar la mesa como ocupada
                mesa.ocupada = True
                mesa.save()

                # Crear el pedido
                nuevo_pedido = Pedido.objects.create(
                    mesa=mesa,
                    estado='pendiente',
                    usuario=request.user
                )

                # Agregar productos al pedido
                for item in productos_validos:
                    PedidoProducto.objects.create(
                        pedido=nuevo_pedido,
                        producto=item['producto'],
                        cantidad=item['cantidad'],
                        precio_unitario=item['precio']
                    )

                    # Actualizar inventario
                    item['inventario'].cantidad -= item['cantidad']
                    item['inventario'].save()

                messages.success(request, 'Pedido creado exitosamente!')
                return redirect('ver_pedidos')
            else:
                messages.error(request, 'No se pudo crear el pedido. Verifica los productos.')

    # Filtrar mesas disponibles (no ocupadas)
    mesas_disponibles = Mesa.objects.filter(sede=sede_usuario, ocupada=False)

    return render(request, 'pedidos/ver_pedidos.html', {
        'pedidos': pedidos,
        'estado': estado,
        'mesas': mesas_disponibles,  # Solo mostrar mesas no ocupadas
        'productos': InventarioProducto.objects.filter(sede=sede_usuario),
    })

# Exportar pedidos a CSV
@login_required
def exportar_csv_pedidos(request):
    if request.user.rol not in ['cajero', 'administrador']:
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


# Editar pedido
@csrf_exempt
@require_http_methods(["POST"])
@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    productos = request.POST.getlist('producto[]')
    cantidades = request.POST.getlist('cantidad[]')

    if not productos or not cantidades or len(productos) != len(cantidades):
        messages.error(request, "Datos inválidos para editar el pedido.")
        return redirect('ver_pedidos')

    total_pedido = 0
    sede = request.user.sede

    for producto_id, cantidad in zip(productos, cantidades):
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                continue

            producto = Producto.objects.get(id=producto_id)
            inventario = InventarioProducto.objects.get(producto=producto, sede=sede)

            if inventario.cantidad < cantidad:
                messages.warning(request, f"No hay suficiente stock de {producto.nombre}.")
                continue

            if not inventario.precio_venta or inventario.precio_venta <= 0:
                messages.warning(request, f"El producto {producto.nombre} no tiene un precio de venta válido.")
                continue

            inventario.cantidad -= cantidad
            inventario.save()

            pedido_producto, created = PedidoProducto.objects.get_or_create(
                pedido=pedido,
                producto=producto,
                defaults={'cantidad': cantidad, 'precio_unitario': inventario.precio_venta}
            )

            if not created:
                pedido_producto.cantidad += cantidad

            pedido_producto.precio_unitario = inventario.precio_venta
            pedido_producto.save()

            total_pedido += inventario.precio_venta * cantidad * Decimal('1.19')

        except Exception as e:
            continue

    pedido.total = total_pedido
    pedido.save()
    messages.success(request, "Pedido editado correctamente.")
    return redirect('ver_pedidos')

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
    if request.user.rol not in ['cajero', 'administrador']:
        return redirect('dashboard')

    try:
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.estado = 'pagado'
        pedido.save()

        # Liberar la mesa
        if pedido.mesa:
            pedido.mesa.ocupada = False
            pedido.mesa.save()

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
