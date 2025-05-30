from django.db import models
from sede.models import Sede
from productos.models import Producto  # Este es el modelo general de productos
from django.core.exceptions import ValidationError

class InventarioProducto(models.Model):  
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)  # Evita valores negativos
    stock_minimo = models.PositiveIntegerField(default=5)
    imagen = models.ImageField(upload_to='inventario/', blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.cantidad < 0:
            raise ValidationError("La cantidad no puede ser negativa.")
        if self.stock_minimo < 0:
            raise ValidationError("El stock mínimo no puede ser negativo.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a `clean()` antes de guardar
        super().save(*args, **kwargs)


    def en_alerta(self):
        return self.cantidad <= self.stock_minimo

    def __str__(self):
        return f"{self.producto.nombre} - {self.sede.nombre}"
