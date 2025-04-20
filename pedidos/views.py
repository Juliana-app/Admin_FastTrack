from rest_framework import generics
from .models import Pedido
from .serializers import PedidoSerializer
from rest_framework.permissions import IsAuthenticated

class PedidoListCreateView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all().order_by('-fecha_creacion')
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

class PedidoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
