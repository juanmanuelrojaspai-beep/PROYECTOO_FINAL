from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils import timezone

from inventario.models import Repuesto
from ventas.models import DetalleVenta, Venta


@staff_member_required
def dashboard(request):
    hoy = timezone.localdate()
    inicio_mes = hoy.replace(day=1)
    hace_7_dias = hoy - timedelta(days=6)

    ventas_hoy = Venta.objects.filter(fecha__date=hoy).aggregate(total=Sum("total"), n=Count("id"))
    ventas_mes = Venta.objects.filter(fecha__date__gte=inicio_mes).aggregate(total=Sum("total"), n=Count("id"))

    ventas_por_dia = (
        Venta.objects.filter(fecha__date__gte=hace_7_dias)
        .annotate(dia=TruncDate("fecha"))
        .values("dia")
        .annotate(total=Sum("total"), n=Count("id"))
        .order_by("dia")
    )

    ingresos = ExpressionWrapper(
        F("cantidad") * F("precio_unitario"),
        output_field=DecimalField(max_digits=14, decimal_places=2),
    )
    mas_vendidos = (
        DetalleVenta.objects.values("repuesto__codigo", "repuesto__nombre")
        .annotate(unidades=Sum("cantidad"), ingresos=Sum(ingresos))
        .order_by("-unidades")[:10]
    )

    stock_bajo = Repuesto.objects.filter(activo=True, stock__lte=F("stock_minimo")).order_by("stock")

    contexto = {
        "ventas_hoy": ventas_hoy,
        "ventas_mes": ventas_mes,
        "ventas_por_dia": ventas_por_dia,
        "mas_vendidos": mas_vendidos,
        "stock_bajo": stock_bajo,
    }
    return render(request, "reportes/dashboard.html", contexto)
