from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F
from django.utils import timezone

from inventario.models import Repuesto


class Proveedor(models.Model):
    nombre = models.CharField(max_length=120)
    nit = models.CharField("NIT", max_length=30, unique=True)
    contacto = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    correo = models.EmailField(blank=True)

    class Meta:
        verbose_name_plural = "proveedores"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name="compras")
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0, editable=False)
    observaciones = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Compra #{self.pk} - {self.proveedor}"

    def recalcular_total(self):
        self.total = sum((d.subtotal for d in self.detalles.all()), Decimal("0"))
        self.save(update_fields=["total"])

    def delete(self, *args, **kwargs):
        # Al borrar una compra se revierte el stock que había sumado
        with transaction.atomic():
            for d in self.detalles.all():
                Repuesto.objects.filter(pk=d.repuesto_id).update(stock=F("stock") - d.cantidad)
            return super().delete(*args, **kwargs)


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="detalles")
    repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.repuesto}"

    @property
    def subtotal(self):
        return self.cantidad * self.costo_unitario

    def clean(self):
        if self.cantidad is not None and self.cantidad < 1:
            raise ValidationError({"cantidad": "La cantidad debe ser al menos 1."})

    def save(self, *args, **kwargs):
        nuevo = self.pk is None
        with transaction.atomic():
            super().save(*args, **kwargs)
            if nuevo:  # Una compra registrada sube el stock
                Repuesto.objects.filter(pk=self.repuesto_id).update(stock=F("stock") + self.cantidad)
