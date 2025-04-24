from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from sede.models import Sede

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CrearUsuarioForm(forms.ModelForm):  # este lo usa el admin para crear usuarios
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'rol', 'sede']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
