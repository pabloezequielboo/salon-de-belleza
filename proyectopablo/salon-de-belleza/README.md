# Proyecto: salon-de-belleza

Este repositorio contiene una pequeña aplicación Django para gestionar reservas/turnos en un salón de belleza.

Estado (19-11-2025):

- Estructura del proyecto ya creada (app `core`, configuración en `salon_de_belleza`).
- Archivos estáticos y plantillas básicas presentes.

Cambios realizados por el asistente (comentados en código):

1. `core/views.py`
   - Añadido parsing seguro de `fecha` y `hora` desde el formulario usando `datetime.strptime`.
   - Conversión a timezone-aware con `timezone.make_aware`.
   - Uso de `nombre_cliente` desde el POST si viene; fallback a "Cliente de Prueba".
   - Comentarios explicativos añadidos para cada paso.

2. `core/models.py`
   - Comentarios/documentación para `Servicio`, `Turno` y `Reserva`.
   - Robustecimiento de `Turno.save()` para calcular `fecha_hora_fin` sólo si `fecha_hora_inicio` existe.
   - Explicación de la diferencia entre `Turno` (modelo relacional) y `Reserva` (modelo simple para el formulario).

3. `core/urls.py` y `core/forms.py`
   - Comentarios y docstrings explicativos añadidos.

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
