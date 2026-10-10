from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reportes/', include('reportes.urls')),
    path('', include('inventario.urls')),
]
