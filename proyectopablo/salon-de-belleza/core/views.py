from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Reserva  # Asegúrate de que este es el modelo que creaste
from django.contrib import messages
from .models import Servicio, Turno

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

        # 3. Comprobar si ya existe un Turno para ese servicio y hora de inicio
        existe = Turno.objects.filter(servicio=servicio, fecha_hora_inicio=fecha_hora_inicio).exists()
        if existe:
            messages.error(request, 'Lo siento, ese turno ya está reservado. Elige otro horario.')
            return redirect('crear_reserva')

        # 4. Crear el Turno con duración fija de 1 hora (intervalo entre inicios de turnos = 1 hora)
        fecha_hora_fin = fecha_hora_inicio + timedelta(hours=1)
        turno = Turno(
            servicio=servicio,
            cliente_nombre=nombre_cliente,
            fecha_hora_inicio=fecha_hora_inicio,
            fecha_hora_fin=fecha_hora_fin,
            confirmado=False,
        )
        turno.save()

        # (Opcional) también puedes crear una entrada en Reserva si quieres mantener ambos modelos
        Reserva.objects.create(servicio=servicio.nombre, nombre_cliente=nombre_cliente, fecha_hora=fecha_hora_inicio)

        messages.success(request, 'Reserva creada correctamente.')
        return redirect('reserva_exitosa')

    # Si es GET: mostrar el formulario con la lista de servicios y horarios por hora
    servicios = Servicio.objects.all()

    # Generar opciones horarias cada hora (ej: 09:00 a 17:00)
    horas = []
    for h in range(9, 18):
        horas.append(f"{h:02d}:00")

    return render(request, 'core/reservar_turno.html', {'servicios': servicios, 'horas': horas})


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

        # En un proyecto real enviarías un email o guardarías el mensaje.
        # Aquí sólo mostramos un mensaje de éxito al usuario.
        messages.success(request, 'Gracias, hemos recibido tu mensaje. Te responderemos pronto.')
        return redirect('contacto')

    return render(request, 'core/contacto.html')


def reserva_exitosa_view(request):
    """
    Muestra una página de confirmación de reserva exitosa.
    """
    return render(request, 'core/reserva_exitosa.html')  # Necesitarás crear esta plantilla