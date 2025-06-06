from decimal import Decimal
from django.db import models
from django.utils import timezone
from inventario.models import Producto
from mesa.models import Mesa
from usuarios.models import Usuario

ESTADOS_PEDIDO = [
    ('pendiente', 'Pendiente'),

    ('pagado', 'Pagado'),
]

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True)
    pagado = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa}"
    
    def marcar_pagado(self):  
        self.estado = 'pagado'
        if self.mesa:
            self.mesa.ocupada = False
            self.mesa.save()
        self.save()

class PedidoProducto(models.Model):
    pedido = models.ForeignKey('Pedido', related_name='productos', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def subtotal_con_iva(self):
        return self.precio_unitario * self.cantidad * Decimal('1.19')

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido {self.pedido.id})"
