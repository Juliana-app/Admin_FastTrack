from django.contrib.auth.models import AbstractUser
from django.db import models
from sede.models import Sede

ROLES = [
    ('mesero', 'Mesero'),
    ('cajero', 'Cajero'),
    ('administrador', 'Administrador'),
]

class Usuario(AbstractUser):
    rol = models.CharField(max_length=20, choices=ROLES)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()}) - {self.sede.nombre if self.sede else 'Sin sede'}"
