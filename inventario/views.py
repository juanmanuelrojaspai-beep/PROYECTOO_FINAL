from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Categoria, Repuesto


def catalogo(request):
    """Lista de repuestos con búsqueda, filtro por categoría y páginas."""
    q = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "")

    repuestos = Repuesto.objects.filter(activo=True).select_related("categoria", "marca")

    if q:  # busca por nombre, código o por la moto compatible
        repuestos = repuestos.filter(
            Q(nombre__icontains=q)
            | Q(codigo__icontains=q)
            | Q(motos__marca__icontains=q)
            | Q(motos__modelo__icontains=q)
        ).distinct()

    if categoria.isdigit():
        repuestos = repuestos.filter(categoria_id=categoria)

    pagina = Paginator(repuestos, 12).get_page(request.GET.get("page"))

    contexto = {
        "pagina": pagina,
        "categorias": Categoria.objects.all(),
        "q": q,
        "categoria_sel": categoria,
    }
    return render(request, "inventario/catalogo.html", contexto)


def detalle(request, pk):
    """Página de un solo repuesto."""
    repuesto = get_object_or_404(
        Repuesto.objects.select_related("categoria", "marca").prefetch_related("motos"),
        pk=pk, activo=True,
    )
    return render(request, "inventario/detalle.html", {"repuesto": repuesto})
