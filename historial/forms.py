# historial/forms.py
from django import forms
from historial.models import HistorialPrecio

class PrecioForm(forms.ModelForm):
    class Meta:
        model = HistorialPrecio
        fields = ['producto', 'precio_compra', 'precio_venta']