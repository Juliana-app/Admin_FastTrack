from django.db import models
from django.utils import timezone
from inventario.models import Producto
from usuarios.models import Usuario

ESTADOS_PEDIDO = [
    ('pendiente', 'Pendiente'),
    ('preparando', 'Preparando'),
    ('servido', 'Servido'),
    ('pagado', 'Pagado'),
]

class Pedido(models.Model):
    mesero = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, limit_choices_to={'rol': 'mesero'})
    mesa = models.CharField(max_length=10)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa}"

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido {self.pedido.id})"
