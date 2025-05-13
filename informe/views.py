from django.shortcuts import render
from django.db.models import Sum,F, ExpressionWrapper, DecimalField, OuterRef, Subquery
from pedidos.models import PedidoProducto
from django.contrib.auth.decorators import login_required
from historial.models import HistorialPrecio
import csv
from datetime import datetime
from django.http import HttpResponse

@login_required
def listar_informes(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Selección eficiente de relaciones
    pedidos = PedidoProducto.objects.select_related(
        'producto',  # Relacionamos con Producto
        'pedido__mesa__sede'  # Relacionamos con Sede
    ).values(
        'producto__id',  # Obtenemos el id del producto
        'producto__nombre',  # Obtenemos el nombre del producto
        'pedido__mesa__sede__nombre'  # Obtenemos el nombre de la sede
    ).annotate(
        cantidad_vendida=Sum('cantidad')  # Sumamos las cantidades vendidas
    )

    # Filtro por fechas
    if fecha_inicio:
        pedidos = pedidos.filter(pedido__creado__gte=fecha_inicio)
    if fecha_fin:
        pedidos = pedidos.filter(pedido__creado__lte=fecha_fin)

    informes = []

    for pedido in pedidos:
        producto_id = pedido['producto__id']
        producto_nombre = pedido['producto__nombre']
        sede_nombre = pedido['pedido__mesa__sede__nombre']
        cantidad_vendida = pedido['cantidad_vendida']

        # Obtener el historial de precios del producto
        historial = HistorialPrecio.objects.filter(producto_id=producto_id).last()

        # Si no existe un historial, asignamos valores predeterminados
        precio_compra = historial.precio_compra if historial else 0
        precio_venta = historial.precio_venta if historial else 0

        # Calcular la ganancia de manera correcta
        ganancia = (precio_venta - precio_compra) * cantidad_vendida

        informes.append({
            'producto_id': producto_id,
            'producto_nombre': producto_nombre,
            'sede_nombre': sede_nombre,
            'cantidad_vendida': cantidad_vendida,
            'precio_compra': precio_compra,
            'precio_venta': precio_venta,
            'ganancia': ganancia
        })

    return render(request, 'informes/listar_informes.html', {'informes': informes})

@login_required
def exportar_csv(request):
    from django.db.models import Sum
    from pedidos.models import PedidoProducto
    from historial.models import HistorialPrecio
    from datetime import datetime
    import csv
    from django.http import HttpResponse

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    pedidos = PedidoProducto.objects.select_related(
        'producto',
        'pedido__usuario__sede'
    ).values(
        'producto__id',
        'producto__nombre',
        'pedido__usuario__sede__nombre'
    ).annotate(
        cantidad_vendida=Sum('cantidad')
    )

    if fecha_inicio:
        pedidos = pedidos.filter(pedido__creado__gte=fecha_inicio)
    if fecha_fin:
        pedidos = pedidos.filter(pedido__creado__lte=fecha_fin)

    resumen = []

    for p in pedidos:
        producto_id = p['producto__id']
        producto_nombre = p['producto__nombre']
        sede_nombre = p['pedido__usuario__sede__nombre']
        cantidad_vendida = p['cantidad_vendida']

        # Obtener último historial válido
        historial = HistorialPrecio.objects.filter(producto_id=producto_id).order_by('-fecha').first()
        precio_compra = historial.precio_compra if historial else 0
        precio_venta = historial.precio_venta if historial else 0

        ganancia = (precio_venta - precio_compra) * cantidad_vendida

        resumen.append({
            'producto_id': producto_id,
            'producto_nombre': producto_nombre,
            'cantidad_vendida': cantidad_vendida,
            'sede_nombre': sede_nombre,
            'precio_compra': precio_compra,
            'precio_venta': precio_venta,
            'ganancia': ganancia
        })

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="informe_ventas.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID Producto', 'Producto', 'Cantidad Vendida', 'Sede', 'Precio Compra', 'Precio Venta', 'Ganancia'])

    for r in resumen:
        writer.writerow([
            r['producto_id'],
            r['producto_nombre'],
            r['cantidad_vendida'],
            r['sede_nombre'],
            f"{r['precio_compra']:.2f}",
            f"{r['precio_venta']:.2f}",
            f"{r['ganancia']:.2f}"
        ])

    return response
