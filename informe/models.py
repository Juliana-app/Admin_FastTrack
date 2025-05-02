# informe/models.py

from django.db import models
from productos.models import Producto
from inventario.models import InventarioProducto
from pedidos.models import PedidoProducto
from historial.models import HistorialPrecio

class InformeProducto:
    def __init__(self, producto_id, nombre, cantidad_vendida, sede, precio_compra, precio_venta):
        self.producto_id = producto_id
        self.nombre = nombre
        self.cantidad_vendida = cantidad_vendida
        self.sede = sede
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.ganancia = (self.precio_venta - self.precio_compra) * self.cantidad_vendida
