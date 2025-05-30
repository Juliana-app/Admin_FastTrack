from django import forms
from .models import InventarioProducto
from sede.models import Sede

class ProductoInventarioForm(forms.ModelForm):
    sede = forms.ModelChoiceField(queryset=Sede.objects.all(), required=False)

    class Meta:
        model = InventarioProducto
        fields = ['producto', 'cantidad', 'stock_minimo', 'imagen', 'sede']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None and user.rol != 'administrador':
            # Si NO es admin, ocultar o quitar el campo sede
            self.fields.pop('sede')

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return cantidad

    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo is not None and stock_minimo < 0:
            raise forms.ValidationError("El stock mínimo no puede ser negativo.")
        return stock_minimo
