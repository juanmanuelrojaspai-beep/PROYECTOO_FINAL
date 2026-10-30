from rest_framework import viewsets

from .models import Compra, Proveedor
from .serializers import CompraSerializer, ProveedorSerializer


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer


class CompraViewSet(viewsets.ReadOnlyModelViewSet):   # solo consulta
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer