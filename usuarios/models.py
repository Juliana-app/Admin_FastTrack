from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('mesero', 'Mesero'),
    ('cajero', 'Cajero'),
    ('admin', 'Administrador'),
]

class Usuario(AbstractUser):
    rol = models.CharField(max_length=10, choices=ROLES)
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
