from django.db import models
from productos.models import Producto

class HistorialPrecio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.nombre} - Compra: ${self.precio_compra} | Venta: ${self.precio_venta} ({self.fecha.strftime('%Y-%m-%d')})"
