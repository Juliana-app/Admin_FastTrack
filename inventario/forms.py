from django import forms
from .models import InventarioProducto

class ProductoInventarioForm(forms.ModelForm):
    class Meta:
        model = InventarioProducto
        fields = ['producto', 'cantidad', 'stock_minimo', 'imagen']

