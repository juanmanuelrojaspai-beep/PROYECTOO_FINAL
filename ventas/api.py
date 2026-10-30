from rest_framework import viewsets

from .models import Venta
from .serializers import VentaSerializer


class VentaViewSet(viewsets.ReadOnlyModelViewSet):    # solo consulta
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer