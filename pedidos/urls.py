from django.urls import path

from Admin_Bar_FastTrack import views
from .views import (
    PedidoListCreateView, PedidoDetailView, editar_pedido, 
    exportar_csv_pedidos,
    pedidos_por_pagar, tomar_pedido, ver_pedidos, vista_cajero
)

from . import views


urlpatterns = [
    path('', PedidoListCreateView.as_view(), name='listar_crear_pedidos'),
    path('<int:pk>/', PedidoDetailView.as_view(), name='detalle_pedido'),
    path('tomar/', tomar_pedido, name='tomar_pedido'),
    path('ver/', ver_pedidos, name='ver_pedidos'),
    path('exportar/', exportar_csv_pedidos, name='exportar_csv'),
    path('editar/<int:pedido_id>/', editar_pedido, name='editar_pedido'),
    path('por_pagar/', pedidos_por_pagar, name='pedidos_por_pagar'),
    path('marcar_pagado/<int:pedido_id>/', views.marcar_pedido_pagado, name='marcar_pedido_pagado'),
    path('mesero/', ver_pedidos, name='ver_pedidos_mesero'),
    path('caja/', vista_cajero, name='dashboard_caja'),
]
