from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # La ruta para el panel de administración de Django.
    path('admin/', admin.site.urls),

    # Incluye las URLs de la aplicación 'core'
    path('', include('core.urls')),
]
