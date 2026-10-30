from rest_framework import serializers

from .models import DetalleVenta, Venta


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ["repuesto", "cantidad", "precio_unitario"]


class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = ["id", "cliente", "vendedor", "fecha", "metodo_pago", "total", "detalles"]