"""
core.views
-----------
Vistas principales del app `core`.

Cambios importantes realizados:
- `reservar_turno_view`: genera franjas horarias dinámicas según
    `RESERVATION_START_HOUR`, `RESERVATION_END_HOUR` y
    `RESERVATION_SLOT_DURATION_MINUTES` en `settings.py`.
    - Valida y parsea `fecha`+`hora` de forma segura y convierte a timezone-aware.
    - Valida solapamientos entre turnos.
    - Valida que al menos `cliente_telefono` o `cliente_email` esté presente.
    - Crea un `Turno` con `fecha_hora_fin` calculada.
- `contacto_view`: guarda envíos en el nuevo modelo `Contacto`.

Se añadieron mensajes `messages` para feedback al usuario.
"""

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from .models import Contacto, Servicio, Turno  # Contacto: nuevo modelo
from django.contrib import messages

# Nota: Este archivo contiene las vistas (handlers) que responden a las
# peticiones HTTP. Aquí añadimos comentarios y una validación básica
# para parsear la fecha y la hora que vienen desde el formulario.

def index(request):
    """
    Muestra la página de inicio del salón de belleza.
    """
    return render(request, 'core/index.html')


def reservar_turno_view(request):
    # Queremos ofrecer franjas horarias separadas por 1 hora (por ejemplo 09:00,10:00,...)
    # y crear un objeto Turno con duración fija de 1 hora para cada reserva.
    if request.method == 'POST':
        # 1. Obtener los datos del formulario
        servicio_id = request.POST.get('servicio')
        fecha_str = request.POST.get('fecha')
        hora_str = request.POST.get('hora')
        nombre_cliente = request.POST.get('nombre_cliente', 'Cliente de Prueba')
        cliente_telefono = request.POST.get('cliente_telefono', '').strip()
        cliente_email = request.POST.get('cliente_email', '').strip()

        # 2. Parsear fecha y hora en un objeto datetime aware
        if not (servicio_id and fecha_str and hora_str):
            messages.error(request, 'Por favor completa todos los campos.')
            return redirect('crear_reserva')

        try:
            servicio = Servicio.objects.get(id=servicio_id)
        except Servicio.DoesNotExist:
            messages.error(request, 'Servicio no válido.')
            return redirect('crear_reserva')

        try:
            combined = f"{fecha_str} {hora_str}"
            fecha_hora_inicio = datetime.strptime(combined, '%Y-%m-%d %H:%M')
            fecha_hora_inicio = timezone.make_aware(fecha_hora_inicio)
        except Exception:
            messages.error(request, 'Formato de fecha/hora no válido.')
            return redirect('crear_reserva')

        # Validación: el campo teléfono es obligatorio según requerimiento
        if not cliente_telefono:
            messages.error(request, 'El campo Teléfono es obligatorio.')
            return redirect('crear_reserva')

        # 3. Comprobar solapamientos: buscamos cualquier Turno que se solape
        #    con el intervalo [fecha_hora_inicio, fecha_hora_inicio + 1h).
        nueva_fin = fecha_hora_inicio + timedelta(hours=1)

        # Condición para solapamiento: existing.start < new_end and existing.end > new_start
        solapamiento = Turno.objects.filter(
            servicio=servicio,
            fecha_hora_inicio__lt=nueva_fin,
            fecha_hora_fin__gt=fecha_hora_inicio,
        ).exists()

        if solapamiento:
            messages.error(request, 'Lo siento, ese horario se solapa con otra reserva. Elige otro horario.')
            return redirect('crear_reserva')

        # 4. Crear el Turno con duración fija de 1 hora
        turno = Turno(
            servicio=servicio,
            cliente_nombre=nombre_cliente,
            cliente_telefono=cliente_telefono,
            cliente_email=cliente_email,
            fecha_hora_inicio=fecha_hora_inicio,
            fecha_hora_fin=nueva_fin,
            confirmado=False,
        )
        turno.save()

        # Nota: ya no creamos automáticamente una entrada en `Reserva` para evitar
        # duplicar la información. `Turno` es ahora la fuente de verdad para reservas.

        messages.success(request, 'Reserva creada correctamente.')
        return redirect('reserva_exitosa')

    # Si es GET: mostrar el formulario con la lista de servicios y horarios por hora
    servicios = Servicio.objects.all()

    # Generar opciones horarias usando la configuración en settings y el tamaño
    # de cada franja en minutos (p. ej. 60 para 1 hora, 30 para medios horarios).
    start = getattr(settings, 'RESERVATION_START_HOUR', 9)
    end = getattr(settings, 'RESERVATION_END_HOUR', 18)  # valor exclusivo
    slot_minutes = getattr(settings, 'RESERVATION_SLOT_DURATION_MINUTES', 60)

    # Permitir que se preseleccione un servicio mediante query param `?servicio=<id>`
    selected_servicio_id = None
    try:
        qs = request.GET.get('servicio')
        if qs:
            selected_servicio_id = int(qs)
    except Exception:
        selected_servicio_id = None

    horas = []
    # iteramos en minutos desde start*60 hasta end*60 en pasos de slot_minutes
    for minutes in range(start * 60, end * 60, slot_minutes):
        h = minutes // 60
        m = minutes % 60
        horas.append(f"{h:02d}:{m:02d}")

    return render(request, 'core/reservar_turno.html', {'servicios': servicios, 'horas': horas, 'selected_servicio_id': selected_servicio_id})


def servicios_view(request):
    """
    Página que muestra los servicios disponibles.
    Actualmente renderiza una plantilla estática; en el futuro se podría
    listar dinámicamente los objetos `Servicio` desde la BD.
    """
    servicios = Servicio.objects.all()
    return render(request, 'core/servicios.html', {'servicios': servicios})


def contacto_view(request):
    """
    Vista para mostrar y procesar el formulario de contacto.
    En este ejemplo, al enviar el formulario mostramos un mensaje y
    redirigimos a la misma página (puedes adaptarlo para enviar emails).
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        # Guardar en la base de datos para revisión por el equipo
        try:
            Contacto.objects.create(nombre=nombre, email=email, mensaje=mensaje)
            messages.success(request, 'Gracias, hemos recibido tu mensaje. Te responderemos pronto.')
        except Exception:
            # Si hay un error al guardar, notificamos al usuario de forma genérica
            messages.error(request, 'Ocurrió un error al enviar el mensaje. Intenta nuevamente más tarde.')
        return redirect('contacto')

    return render(request, 'core/contacto.html')


def reserva_exitosa_view(request):
    """
    Muestra una página de confirmación de reserva exitosa.
    """
    return render(request, 'core/reserva_exitosa.html')  # Necesitarás crear esta plantilla