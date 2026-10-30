from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from clientes.api import ClienteViewSet
from inventario.api import CategoriaViewSet, MotoViewSet, RepuestoViewSet
from proveedores.api import CompraViewSet, ProveedorViewSet
from ventas.api import VentaViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet)
router.register("motos", MotoViewSet)
router.register("repuestos", RepuestoViewSet)
router.register("clientes", ClienteViewSet)
router.register("proveedores", ProveedorViewSet)
router.register("compras", CompraViewSet)
router.register("ventas", VentaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),              # <- la API
    path('reportes/', include('reportes.urls')),
    path('', include('inventario.urls')),
]