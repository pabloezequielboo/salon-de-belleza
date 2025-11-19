# Proyecto: salon-de-belleza

Este repositorio contiene una pequeña aplicación Django para gestionar reservas/turnos en un salón de belleza.

Estado (19-11-2025):

- Estructura del proyecto ya creada (app `core`, configuración en `salon_de_belleza`).
- Archivos estáticos y plantillas básicas presentes.

Cambios realizados por el asistente (resumen completo):

Modelos (`core/models.py`)
- `Servicio`:
   - Campos añadidos: `descripcion` y `precio`.
   - `__str__` para mostrar el nombre.
- `Turno`:
   - Nuevos campos: `cliente_telefono`, `cliente_email`.
   - Validación: `clean()` exige al menos teléfono o email.
   - `save()` calcula `fecha_hora_fin` automáticamente a partir de
      `servicio.duracion_minutos` y detecta cambios en `confirmado` para crear
      o eliminar una `Reserva` asociada.
   - `delete()` elimina la `Reserva` asociada para evitar registros huérfanos.
- `Reserva`:
   - Se migró de un `CharField` con choices a una `ForeignKey` a `Servicio`.
   - Se añadió `turno` como `OneToOneField` (nullable) para enlazar reserva y turno.
- `Contacto`:
   - Nuevo modelo para almacenar los mensajes enviados desde el formulario de contacto.

Vistas (`core/views.py`)
- `reservar_turno_view`:
   - Parseo seguro de fecha y hora, conversión a timezone-aware.
   - Generación dinámica de franjas horarias según las settings: `RESERVATION_START_HOUR`,
      `RESERVATION_END_HOUR`, `RESERVATION_SLOT_DURATION_MINUTES`.
   - Validación de solapamientos entre turnos.
   - Validación para requerir al menos teléfono o email antes de crear un `Turno`.
- `contacto_view`:
   - Guarda envíos en el modelo `Contacto` y muestra mensajes al usuario.

Admin (`core/admin.py`)
- `ServicioAdmin`: muestra y permite editar `precio` y `descripcion`.
- `TurnoAdmin`: incluye `cliente_telefono` y `cliente_email` en `list_display`.
   - Añadidas acciones: `Confirmar turnos y convertir a reservas` y
      `Cancelar turnos y eliminar reservas`. Estas acciones utilizan
      `Turno.save()` para crear/borrar `Reserva`.
- `ReservaAdmin`: administración básica.
- `Contacto` registrado en admin.

Front-end y plantillas
- `templates/base.html`: ya incorpora `meta viewport` y usa Bootstrap 5.
- `templates/core/reservar_turno.html`:
   - El formulario de reserva se centra vertical y horizontalmente en pantalla.
   - Se aumentó el espaciado entre campos (`mb-3` ampliado por CSS).
   - Los campos `cliente_telefono` y `cliente_email` ya no son ambos `required`;
      la validación se realiza en la vista y en el modelo.
- `static/css/style.css`: añadidas media queries y clases
   (`reservation-wrapper`, `reservation-card`) para centrar el formulario y
   mejorar la respuesta en móviles.

Migraciones y datos
- Se creó y aplicó la migración `0004_contacto` (nuevo modelo Contacto).
- Se creó la migración de datos `0005_convert_reserva_servicio_to_fk` que
   convierte los valores antiguos de `Reserva.servicio` (strings) a referencias
   a instancias `Servicio` (creando servicios si no existían).
- Se aplicó `0006_reserva_turno` para añadir el campo `turno`.

Consideraciones y notas
- Las migraciones intentan preservar datos existentes; revisa la tabla
   `Servicios` en admin para ajustar nombres/precios creados automáticamente.
- Las validaciones de teléfono pueden mejorarse (regex/mask); puedo
   implementarlo si lo deseas.


Operaciones realizadas automáticamente (por el asistente):

- Se creó `requirements.txt` con `Django>=4.2`.
- Se creó este `README.md` para registrar cambios y pasos.

Próximos pasos (ejecutados ahora por el asistente):

- Crear y activar un entorno virtual `.venv`.
- Actualizar `pip` y `pip install -r requirements.txt`.
- Ejecutar `python manage.py migrate`.

Comandos utilizados (PowerShell):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; \
python -m venv .venv; \
.\.venv\Scripts\Activate.ps1; \
python -m pip install --upgrade pip; \
pip install -r requirements.txt; \
python manage.py migrate
```

Notas importantes:

- `createsuperuser` no se ejecutó automáticamente porque es interactivo; puedes ejecutarlo manualmente si necesitas una cuenta admin.
- El servidor de desarrollo (`runserver`) no fue dejado en ejecución por defecto; si quieres que lo inicie en background, dímelo y lo arranco.

Si quieres que siga y arranque el servidor en background, o que cree un superusuario automáticamente (pasando credenciales no seguras), indícalo y lo hago.

---

Acciones ejecutadas ahora (salón-de-belleza/.venv):

- Se creó un entorno virtual en `salon-de-belleza/.venv`.
- Se actualizó `pip` dentro del entorno virtual.
- Se instaló Django (versión instalada: Django-5.2.8) desde `requirements.txt`.
- Se ejecutaron las migraciones y la migración inicial de la app `core` se aplicó correctamente (`core.0001_initial`).

Cómo activar el entorno y arrancar el servidor (PowerShell):

```powershell
# Desde la carpeta del proyecto
cd salon-de-belleza
# Activar entorno
.\.venv\Scripts\Activate.ps1
# Arrancar servidor
python manage.py runserver
```

Si quieres que inicie el servidor ahora en background o que cree el superusuario, confirmamelo y lo hago.
