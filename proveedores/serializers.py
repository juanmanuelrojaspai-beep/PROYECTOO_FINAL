from rest_framework import serializers

from .models import Compra, DetalleCompra, Proveedor


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = "__all__"


class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = ["repuesto", "cantidad", "costo_unitario"]


class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ["id", "proveedor", "fecha", "total", "observaciones", "detalles"]