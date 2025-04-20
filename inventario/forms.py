from django import forms
from .models import InventarioProducto

class ProductoInventarioForm(forms.ModelForm):
    class Meta:
        model = InventarioProducto
        fields = ['producto', 'sede', 'imagen', 'cantidad', 'stock_minimo']
