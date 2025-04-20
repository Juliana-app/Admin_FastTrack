from django.urls import path
from .views import PedidoListCreateView, PedidoDetailView, exportar_csv_pedidos, marcar_pagado, tomar_pedido, ver_pedidos

urlpatterns = [
    path('', PedidoListCreateView.as_view(), name='listar_crear_pedidos'),
    path('<int:pk>/', PedidoDetailView.as_view(), name='detalle_pedido'),
    path('tomar/', tomar_pedido, name='tomar_pedido'),
    path('tomar/', tomar_pedido, name='tomar_pedido'),
    path('ver/', ver_pedidos, name='ver_pedidos'),
    path('pagar/<int:pedido_id>/', marcar_pagado, name='marcar_pagado'),
    path('exportar/', exportar_csv_pedidos, name='exportar_csv'),
]
