from django.contrib import admin

from .models import Categoria, MarcaRepuesto, Moto, Repuesto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nombre",)


@admin.register(MarcaRepuesto)
class MarcaRepuestoAdmin(admin.ModelAdmin):
    search_fields = ("nombre",)


@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ("marca", "modelo", "cilindraje", "anio")
    list_filter = ("marca",)
    search_fields = ("marca", "modelo")


@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "categoria", "marca", "precio_venta", "stock", "stock_minimo", "activo")
    list_filter = ("categoria", "marca", "activo")
    search_fields = ("codigo", "nombre")
    filter_horizontal = ("motos",)

