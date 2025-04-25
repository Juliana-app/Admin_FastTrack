from django.db import models
from sede.models import Sede  

class Mesa(models.Model):
    UBICACIONES = (
        (1, 'Primer piso'),
        (2, 'Segundo piso'),
    )

    numeroMesa = models.PositiveIntegerField()
    capacidad = models.PositiveIntegerField()
    ubicacion = models.IntegerField(choices=UBICACIONES)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    ocupada = models.BooleanField(default=False)

    def __str__(self):
        return f"Mesa {self.numeroMesa} - {self.sede.nombre}"

    class Meta:
        unique_together = ('numeroMesa', 'sede')  # Evitar duplicados en una sede   
