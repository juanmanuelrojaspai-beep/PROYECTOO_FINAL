from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Categoria, Moto, Repuesto
from .serializers import CategoriaSerializer, MotoSerializer, RepuestoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]   # cualquiera lee, solo logueados modifican


class MotoViewSet(viewsets.ModelViewSet):
    queryset = Moto.objects.all()
    serializer_class = MotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RepuestoViewSet(viewsets.ModelViewSet):
    queryset = Repuesto.objects.select_related("categoria", "marca").prefetch_related("motos")
    serializer_class = RepuestoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["codigo", "nombre"]               # /api/repuestos/?search=bujia