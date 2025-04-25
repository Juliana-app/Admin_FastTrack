from django.contrib import admin
from .models import Mesa

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ['numeroMesa', 'capacidad', 'ubicacion', 'sede', 'ocupada']
    list_filter = ['sede', 'ubicacion', 'ocupada']
    search_fields = ['numeroMesa']
