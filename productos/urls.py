# productos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_producto_general, name='crear_producto'),
]
