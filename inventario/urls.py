from django.urls import path

from . import views
from .views import ProductoListCreateView, ProductoUpdateView, crear_producto_inventario, dashboard_general, editar_producto_modal, eliminar_producto, lista_productos

urlpatterns = [
    path('', ProductoListCreateView.as_view(), name='listar_crear'),
    path('<int:pk>/', ProductoUpdateView.as_view(), name='actualizar'),
    path('panel/', dashboard_general, name='dashboard_general'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/editar/<int:pk>/', editar_producto_modal, name='editar_producto_inventario'),
    path('productos/eliminar/<int:pk>/', eliminar_producto, name='eliminar_producto_inventario'),
    path('productos/crear/', crear_producto_inventario, name='crear_inventario'), 
]
