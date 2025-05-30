from django import forms
from historial.models import HistorialPrecio

class PrecioForm(forms.ModelForm):
    class Meta:
        model = HistorialPrecio
        fields = ['producto', 'precio_compra', 'precio_venta']

    def clean_precio_compra(self):
        precio = self.cleaned_data.get('precio_compra')
        if precio is None or precio < 0:
            raise forms.ValidationError("El precio de compra debe ser un número positivo.")
        return precio

    def clean_precio_venta(self):
        precio = self.cleaned_data.get('precio_venta')
        if precio is None or precio < 0:
            raise forms.ValidationError("El precio de venta debe ser un número positivo.")
        return precio
