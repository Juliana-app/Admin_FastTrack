from rest_framework import generics
from .models import Producto
from .serializers import ProductoSerializer

class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoUpdateView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
