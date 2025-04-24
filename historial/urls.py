# historial/urls.py
from django.urls import path
from .views import registrar_precio

urlpatterns = [
    path('crear/', registrar_precio, name='registrar_precio'),
]
