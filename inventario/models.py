from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    stock_minimo = models.IntegerField(default=5)

    def __str__(self):
        return self.nombre
