from django.urls import path

from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("repuesto/<int:pk>/", views.detalle, name="detalle"),
]

