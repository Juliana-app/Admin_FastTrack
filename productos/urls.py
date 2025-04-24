# productos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_producto_general, name='crear_producto'),
    path('editar/<int:pk>/', views.editar_producto_general, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto_general, name='eliminar_producto'),
]
