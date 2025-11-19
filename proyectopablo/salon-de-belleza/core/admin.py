"""
core.admin
----------
Registro de modelos en el panel de administración y acciones personalizadas.

Cambios realizados:
- `ServicioAdmin`: añadido `precio` y `descripcion` en la vista de edición.
- `TurnoAdmin`: muestra `cliente_telefono` y `cliente_email` en la lista; se
    añadieron acciones de admin para confirmar/cancelar turnos en masa. Estas
    acciones aprovechan la lógica de `Turno.save()` para crear/eliminar `Reserva`.
- `ReservaAdmin`: administración básica de reservas.
- `Contacto`: registrado para poder revisar mensajes enviados desde la web.
"""

from django.contrib import admin
from .models import Servicio, Reserva, Turno, Contacto


# Registro del modelo Servicio en el admin
# Esto permite a cualquier superusuario crear, editar y eliminar instancias
# de `Servicio` desde la interfaz de administración de Django.
class ServicioAdmin(admin.ModelAdmin):
    # Campos mostrados en la lista de objetos del admin
    list_display = ('nombre', 'duracion_minutos', 'precio')
    # Habilita búsqueda por nombre
    search_fields = ('nombre', 'descripcion')
    # Orden por defecto en la lista
    ordering = ('nombre',)
    # Mostrar campos en el formulario de edición
    fields = ('nombre', 'descripcion', 'duracion_minutos', 'precio')


# Registro del modelo Reserva en el admin con algunas utilidades
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'nombre_cliente', 'fecha_hora')
    list_filter = ('servicio', 'fecha_hora')
    search_fields = ('nombre_cliente', 'servicio')


# Registro del modelo Turno para que el admin también pueda gestionar turnos
# directamente desde la interfaz (crear, editar, borrar).
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('cliente_nombre', 'cliente_telefono', 'cliente_email', 'servicio', 'fecha_hora_inicio', 'fecha_hora_fin', 'confirmado')
    list_filter = ('servicio', 'confirmado')
    search_fields = ('cliente_nombre', 'servicio__nombre', 'cliente_telefono', 'cliente_email')
    # Mostrar campos en el formulario de edición de Turno
    fields = ('servicio', 'cliente_nombre', 'cliente_telefono', 'cliente_email', 'fecha_hora_inicio', 'fecha_hora_fin', 'confirmado')

    actions = ['confirmar_turnos', 'cancelar_turnos']

    def confirmar_turnos(self, request, queryset):
        """Acción de admin: marcar turnos como confirmados y crear Reserva asociada."""
        updated = 0
        for turno in queryset:
            if not turno.confirmado:
                turno.confirmado = True
                turno.save()
                updated += 1
        self.message_user(request, f"{updated} turno(s) confirmados y convertidos a reservas.")
    confirmar_turnos.short_description = 'Confirmar turnos y convertir a reservas'

    def cancelar_turnos(self, request, queryset):
        """Acción de admin: marcar turnos como no confirmados y eliminar Reserva asociada."""
        updated = 0
        for turno in queryset:
            if turno.confirmado:
                turno.confirmado = False
                turno.save()
                updated += 1
        self.message_user(request, f"{updated} turno(s) cancelados y reservas eliminadas si existían.")
    cancelar_turnos.short_description = 'Cancelar turnos y eliminar reservas'


# Finalmente registramos los modelos con sus clases Admin
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Turno, TurnoAdmin)
admin.site.register(Contacto)

# NOTAS (comentadas para tu referencia):
# - Una vez registrado `Servicio` con `ServicioAdmin`, entra a /admin/ con tu
#   superusuario (`admin`) y verás la sección "Servicios" donde podrás crear
#   nuevos servicios, editarlos o eliminarlos.
# - Crear y eliminar desde el admin no requiere código adicional; Django
#   proporciona los formularios y acciones CRUD automáticamente.
