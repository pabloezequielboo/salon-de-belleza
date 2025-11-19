Mejoras aplicadas (reservas y servicios) — 19-11-2025

- `servicios.html` ahora lista dinámicamente los servicios desde la base de datos.
- La vista `reservar_turno_view` ahora:
  - Genera franjas horarias usando las constantes `RESERVATION_START_HOUR` y `RESERVATION_END_HOUR` en `salon_de_belleza/settings.py`.
  - Verifica solapamientos reales entre turnos (se bloquea la reserva si el nuevo turno se solapa con otro existente).
  - Crea un `Turno` con duración de 1 hora; ya no se crea una fila duplicada en `Reserva`.

Configuración relevante añadida en `salon_de_belleza/settings.py`:

```py
# Hora de inicio (inclusive)
RESERVATION_START_HOUR = 9
# Hora de fin (exclusive) — por ejemplo 18 genera slots desde 09:00 hasta 17:00
RESERVATION_END_HOUR = 18
```

Cómo probar las nuevas validaciones

1. Inicia el servidor si no está corriendo:

```powershell
cd salon-de-belleza
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

2. Ve a `http://127.0.0.1:8000/servicios/` para comprobar que los servicios aparecen listados.
3. Ve a `http://127.0.0.1:8000/reservar/` y crea una reserva para un servicio a una hora determinada.
4. Intenta crear otra reserva cuyo intervalo se solape con la anterior (por ejemplo, si la primera fue 10:00-11:00 intenta crear a las 10:30 o a las 10:00) — el sistema rechazará solapamientos.

Si quieres que ajuste la franja horaria por defecto o que la duración del turno sea configurable desde los settings o desde el admin, lo implemento a continuación.

Nuevas mejoras (17: precios y duración configurable) — 19-11-2025

- Añadido al modelo `Servicio` los campos:
  - `precio` (DecimalField) para almacenar el precio.
  - `descripcion` (TextField) para una descripción opcional del servicio.

- Se actualizó `core/admin.py` para mostrar `precio` en la lista y permitir editar `descripcion`.

- La duración de cada franja de reserva es ahora configurable desde `salon_de_belleza/settings.py` mediante `RESERVATION_SLOT_DURATION_MINUTES`.
  - Por defecto está en 60 minutos (1 hora). El sistema generará las franjas empezando en `RESERVATION_START_HOUR` hasta `RESERVATION_END_HOUR` en pasos de `RESERVATION_SLOT_DURATION_MINUTES`.

Prueba rápida de precios y descripciones:

1. Ve a `http://127.0.0.1:8000/admin/` y añade o edita algunos `Servicio` estableciendo `precio` y `descripcion`.
2. Abre `http://127.0.0.1:8000/servicios/` y verás los precios y descripciones mostrados en las cards.

Prueba rápida de duración configurable:

1. Cambia temporalmente en `salon_de_belleza/settings.py`:

```py
RESERVATION_SLOT_DURATION_MINUTES = 30
```

2. Reinicia el servidor y abre `http://127.0.0.1:8000/reservar/` — deberías ver slots cada 30 minutos (ej: 09:00, 09:30, 10:00...).
