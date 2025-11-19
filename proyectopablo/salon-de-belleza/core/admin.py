from django.contrib import admin
from .models import Servicio, Reserva, Turno


# Registro del modelo Servicio en el admin
# Esto permite a cualquier superusuario crear, editar y eliminar instancias
# de `Servicio` desde la interfaz de administración de Django.
class ServicioAdmin(admin.ModelAdmin):
    # Campos mostrados en la lista de objetos del admin
    list_display = ('nombre', 'duracion_minutos')
    # Habilita búsqueda por nombre
    search_fields = ('nombre',)
    # Orden por defecto en la lista
    ordering = ('nombre',)


# Registro del modelo Reserva en el admin con algunas utilidades
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'nombre_cliente', 'fecha_hora')
    list_filter = ('servicio', 'fecha_hora')
    search_fields = ('nombre_cliente', 'servicio')


# Registro del modelo Turno para que el admin también pueda gestionar turnos
# directamente desde la interfaz (crear, editar, borrar).
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('cliente_nombre', 'servicio', 'fecha_hora_inicio', 'fecha_hora_fin', 'confirmado')
    list_filter = ('servicio', 'confirmado')
    search_fields = ('cliente_nombre', 'servicio__nombre')


# Finalmente registramos los modelos con sus clases Admin
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Turno, TurnoAdmin)

# NOTAS (comentadas para tu referencia):
# - Una vez registrado `Servicio` con `ServicioAdmin`, entra a /admin/ con tu
#   superusuario (`admin`) y verás la sección "Servicios" donde podrás crear
#   nuevos servicios, editarlos o eliminarlos.
# - Crear y eliminar desde el admin no requiere código adicional; Django
#   proporciona los formularios y acciones CRUD automáticamente.
