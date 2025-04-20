from django.urls import path
from .views import PedidoListCreateView, PedidoDetailView

urlpatterns = [
    path('', PedidoListCreateView.as_view(), name='listar_crear_pedidos'),
    path('<int:pk>/', PedidoDetailView.as_view(), name='detalle_pedido'),
]
