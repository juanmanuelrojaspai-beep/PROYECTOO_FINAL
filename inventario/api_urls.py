from rest_framework.routers import DefaultRouter

from .api import CategoriaViewSet, MotoViewSet, RepuestoViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet)
router.register("motos", MotoViewSet)
router.register("repuestos", RepuestoViewSet)

urlpatterns = router.urls