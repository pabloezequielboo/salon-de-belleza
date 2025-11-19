"""
core.models
---------------
Este módulo contiene los modelos principales del sistema: Servicio, Turno,
Reserva y Contacto.

Lista resumida de los cambios realizados por el asistente:

- Servicio: se añadieron campos `descripcion` y `precio` para mostrar información
    más rica en la UI.
- Turno:
    - Se añadieron campos `cliente_telefono` y `cliente_email` para almacenar
        datos de contacto.
    - Se añadió validación (`clean`) para requerir al menos teléfono o email.
    - `save()` calcula automáticamente `fecha_hora_fin` usando `servicio.duracion_minutos`.
    - `save()` detecta cambios en `confirmado` y crea/elimina una `Reserva` asociada
        cuando corresponde.
    - `delete()` elimina cualquier `Reserva` asociada (por `nombre_cliente` y hora)
        para evitar reservas huérfanas.
- Reserva:
    - Se migró de un CharField (`servicio`) con choices a una ForeignKey a `Servicio`.
    - Se añadió un campo `turno` (OneToOne) para poder enlazar una reserva con su
        turno confirmada.
- Contacto: nuevo modelo para almacenar envíos del formulario de contacto.

Notas sobre migraciones:
- Se creó una migración de datos (`0005_convert_reserva_servicio_to_fk`) que:
    1) añade temporalmente `servicio_fk` (FK nullable), 2) mapea valores de texto
    a instancias de `Servicio` (creando servicios si es necesario), 3) elimina
    el antiguo campo `servicio` y 4) renombra `servicio_fk` a `servicio`.

Estas decisiones buscan mantener compatibilidad con la base de datos existente
sin pérdida de datos y facilitar un modelo relacional consistente.
"""

from django.db import models
from datetime import timedelta


# Modelo que representa un tipo de servicio ofrecido por el salón.
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    duracion_minutos = models.IntegerField(default=30)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre


class Turno(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cliente_nombre = models.CharField(max_length=100)
    cliente_telefono = models.CharField(max_length=20, blank=True)
    cliente_email = models.EmailField(blank=True)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(editable=False)
    confirmado = models.BooleanField(default=False)

    class Meta:
        ordering = ['fecha_hora_inicio']
        unique_together = ('servicio', 'fecha_hora_inicio')

    def __str__(self):
        return f"Turno para {self.cliente_nombre} - {self.servicio.nombre} el {self.fecha_hora_inicio.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        # Validación: al menos teléfono o email
        try:
            self.full_clean()
        except Exception:
            # Dejamos que la excepción suba para que el llamador la maneje
            raise

        # Calcular hora de fin si no está establecida
        if not getattr(self, 'fecha_hora_fin', None) and self.fecha_hora_inicio and self.servicio:
            self.fecha_hora_fin = self.fecha_hora_inicio + timedelta(minutes=self.servicio.duracion_minutos)

        previo = None
        if self.pk:
            try:
                previo = Turno.objects.get(pk=self.pk)
            except Turno.DoesNotExist:
                previo = None

        super().save(*args, **kwargs)

        # Si el turno está confirmado (nuevo o existente), crear o actualizar la Reserva
        if self.confirmado:
            # Obtener o crear la instancia de Servicio relacionada (case-insensitive)
            servicio_obj = Servicio.objects.filter(nombre__iexact=self.servicio.nombre).first()
            if not servicio_obj:
                name = (self.servicio.nombre or '').lower()
                if 'uña' in name or 'uñas' in name:
                    label = 'Uñas'
                elif 'tint' in name:
                    label = 'Tintura'
                elif 'corte' in name:
                    label = 'Corte de Pelo'
                else:
                    label = self.servicio.nombre or 'Servicio'
                servicio_obj, _ = Servicio.objects.get_or_create(nombre=label)

            # Buscar una Reserva existente preferiblemente ya vinculada a este turno
            reserva = Reserva.objects.filter(turno=self).first()
            if not reserva:
                # Si no hay reserva vinculada, intentar encontrar una por nombre+fecha
                reserva = Reserva.objects.filter(nombre_cliente=self.cliente_nombre, fecha_hora=self.fecha_hora_inicio).first()

            if reserva:
                # Actualizar y vincular
                reserva.servicio = servicio_obj
                reserva.turno = self
                reserva.nombre_cliente = self.cliente_nombre
                reserva.fecha_hora = self.fecha_hora_inicio
                reserva.save()
            else:
                # Crear una reserva nueva y vincularla al turno
                Reserva.objects.create(
                    servicio=servicio_obj,
                    turno=self,
                    nombre_cliente=self.cliente_nombre,
                    fecha_hora=self.fecha_hora_inicio,
                )

        # Si antes estaba confirmado y ahora no, eliminar la Reserva asociada (si existe)
        if previo and previo.confirmado and not self.confirmado:
            # Primero intentamos borrar por relación directa `turno`.
            Reserva.objects.filter(turno=self).delete()
            # Como fallback, eliminamos por nombre+fecha en caso de que existan reservas antiguas.
            Reserva.objects.filter(nombre_cliente=self.cliente_nombre, fecha_hora=self.fecha_hora_inicio).delete()

    def delete(self, *args, **kwargs):
        """Al borrar un Turno, también eliminamos la Reserva equivalente si existe.

        Esto mantiene la base de datos consistente sin requerir cambios en el
        esquema de `Reserva` (que en las migraciones iniciales es un CharField).
        """
        # Borramos la reserva asociada por relación directa si existe.
        Reserva.objects.filter(turno=self).delete()
        # Fallback: también borramos por nombre+hora para compatibilidad con registros
        # que pudieran haberse creado antes de la migración a ForeignKey.
        Reserva.objects.filter(nombre_cliente=self.cliente_nombre, fecha_hora=self.fecha_hora_inicio).delete()
        return super().delete(*args, **kwargs)

    def clean(self):
        # Asegurar que el teléfono esté presente (requisito del negocio)
        from django.core.exceptions import ValidationError
        if not (self.cliente_telefono and self.cliente_telefono.strip()):
            raise ValidationError('Debes proporcionar un número de teléfono.')


class Reserva(models.Model):
    # Ahora `Reserva` referencia directamente al modelo `Servicio` para mantener
    # integridad referencial y poder mostrar el precio/descripcion.
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, blank=True)
    turno = models.OneToOneField('Turno', on_delete=models.SET_NULL, null=True, blank=True)

    nombre_cliente = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(verbose_name='Fecha y Hora')

    def __str__(self):
        servicio_nombre = self.servicio.nombre if self.servicio else 'Servicio desconocido'
        return f"{servicio_nombre} - {self.nombre_cliente} ({self.fecha_hora.strftime('%d/%m %H:%M')})"


class Contacto(models.Model):
    """Modelo para almacenar mensajes enviados desde el formulario de contacto."""
    nombre = models.CharField(max_length=150)
    email = models.EmailField()
    mensaje = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} <{self.email}> - {self.creado_en.strftime('%Y-%m-%d %H:%M')}"