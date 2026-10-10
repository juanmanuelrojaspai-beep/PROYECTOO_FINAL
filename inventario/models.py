from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class MarcaRepuesto(models.Model):
    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = "marca de repuesto"
        verbose_name_plural = "marcas de repuesto"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Moto(models.Model):
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=80)
    cilindraje = models.PositiveIntegerField(help_text="En centímetros cúbicos (cc)")
    anio = models.PositiveIntegerField("año")

    class Meta:
        ordering = ["marca", "modelo", "anio"]
        unique_together = ("marca", "modelo", "cilindraje", "anio")

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.cilindraje}cc ({self.anio})"


class Repuesto(models.Model):
    codigo = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="repuestos")
    marca = models.ForeignKey(
        MarcaRepuesto, on_delete=models.PROTECT, null=True, blank=True, related_name="repuestos"
    )
    # Compatibilidad: un repuesto sirve para varias motos y una moto usa muchos repuestos
    motos = models.ManyToManyField(Moto, blank=True, related_name="repuestos")
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

