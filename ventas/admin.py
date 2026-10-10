from django.contrib import admin

from .models import DetalleVenta, Venta


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    autocomplete_fields = ["repuesto"]

    # Las ventas no se editan una vez creadas (así el stock siempre es consistente)
    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj else 1

    def get_readonly_fields(self, request, obj=None):
        return ["repuesto", "cantidad", "precio_unitario"] if obj else []

    def has_add_permission(self, request, obj=None):
        return obj is None

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "cliente", "vendedor", "metodo_pago", "total")
    list_filter = ("metodo_pago", "fecha")
    search_fields = ("cliente__nombre", "cliente__documento")
    autocomplete_fields = ["cliente"]
    readonly_fields = ("vendedor", "total")
    inlines = [DetalleVentaInline]

    def save_model(self, request, obj, form, change):
        if not obj.vendedor_id:
            obj.vendedor = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.recalcular_total()

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)  # el borrado masivo no devuelve el stock
        return actions

