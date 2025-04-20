from rest_framework import serializers
from .models import Pedido, PedidoProducto
from inventario.models import Producto

class PedidoProductoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = PedidoProducto
        fields = ['id', 'producto', 'producto_nombre', 'cantidad']

class PedidoSerializer(serializers.ModelSerializer):
    items = PedidoProductoSerializer(many=True)
    
    class Meta:
        model = Pedido
        fields = ['id', 'mesero', 'mesa', 'estado', 'fecha_creacion', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        pedido = Pedido.objects.create(**validated_data)
        for item in items_data:
            PedidoProducto.objects.create(pedido=pedido, **item)
        return pedido
