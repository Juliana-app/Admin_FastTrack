from django.db import models
from sede.models import Sede
from productos.models import Producto  # Este es el modelo general de productos
from historial.models import HistorialPrecio  # Si lo usás para otros propósitos

class InventarioProducto(models.Model):  
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    cantidad = models.IntegerField()
    stock_minimo = models.IntegerField(default=5)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def en_alerta(self):
        return self.cantidad <= self.stock_minimo

    def __str__(self):
        return f"{self.producto.nombre} - {self.sede.nombre}"
