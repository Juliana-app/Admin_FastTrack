from django import forms
from .models import Mesa

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numeroMesa', 'capacidad', 'ubicacion', 'sede', 'ocupada']
        widgets = {
            'numeroMesa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de mesa'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidad'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'ocupada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
