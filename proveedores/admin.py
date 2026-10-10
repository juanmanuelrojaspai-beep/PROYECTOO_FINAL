from django.contrib import admin

from .models import Compra, DetalleCompra, Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "nit", "contacto", "telefono")
    search_fields = ("nombre", "nit")


class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    autocomplete_fields = ["repuesto"]

    # Las compras no se editan una vez creadas (así el stock siempre es consistente)
    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj else 1

    def get_readonly_fields(self, request, obj=None):
        return ["repuesto", "cantidad", "costo_unitario"] if obj else []

    def has_add_permission(self, request, obj=None):
        return obj is None

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "proveedor", "total")
    list_filter = ("proveedor", "fecha")
    readonly_fields = ("total",)
    inlines = [DetalleCompraInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.recalcular_total()

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)  # el borrado masivo no revierte el stock
        return actions

