from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F
from django.utils import timezone

from clientes.models import Cliente
from inventario.models import Repuesto


class Venta(models.Model):
    class MetodoPago(models.TextChoices):
        EFECTIVO = "EFE", "Efectivo"
        TARJETA = "TAR", "Tarjeta"
        TRANSFERENCIA = "TRA", "Transferencia"

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True, blank=True, related_name="ventas")
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="ventas"
    )
    fecha = models.DateTimeField(default=timezone.now)
    metodo_pago = models.CharField(max_length=3, choices=MetodoPago.choices, default=MetodoPago.EFECTIVO)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0, editable=False)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Venta #{self.pk}"

    def recalcular_total(self):
        self.total = sum((d.subtotal for d in self.detalles.all()), Decimal("0"))
        self.save(update_fields=["total"])

    def delete(self, *args, **kwargs):
        # Al borrar una venta se devuelve el stock
        with transaction.atomic():
            for d in self.detalles.all():
                Repuesto.objects.filter(pk=d.repuesto_id).update(stock=F("stock") + d.cantidad)
            return super().delete(*args, **kwargs)


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    # Se guarda el precio al momento de la venta: los cambios futuros no alteran facturas viejas
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.cantidad} x {self.repuesto}"

    @property
    def subtotal(self):
        return self.cantidad * (self.precio_unitario or Decimal("0"))

    def clean(self):
        if self.repuesto_id is None or self.cantidad is None:
            return
        if self.cantidad < 1:
            raise ValidationError({"cantidad": "La cantidad debe ser al menos 1."})
        if not self.precio_unitario:
            self.precio_unitario = self.repuesto.precio_venta
        if self.pk is None and self.cantidad > self.repuesto.stock:
            raise ValidationError(
                {"cantidad": f"Stock insuficiente de {self.repuesto.nombre}: quedan {self.repuesto.stock}."}
            )

    def save(self, *args, **kwargs):
        nuevo = self.pk is None
        if not self.precio_unitario:
            self.precio_unitario = self.repuesto.precio_venta
        with transaction.atomic():
            super().save(*args, **kwargs)
            if nuevo:  # Una venta registrada baja el stock
                Repuesto.objects.filter(pk=self.repuesto_id).update(stock=F("stock") - self.cantidad)

