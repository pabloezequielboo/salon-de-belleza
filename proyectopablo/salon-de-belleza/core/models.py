from django.db import models
from django.utils import timezone
from datetime import timedelta


# Modelo que representa un tipo de servicio ofrecido por el salón.
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    duracion_minutos = models.IntegerField(default=30)

    def __str__(self):
        return self.nombre


# Modelo que representa un turno concreto reservado para un servicio.
# - `fecha_hora_inicio` es el comienzo del turno.
# - `fecha_hora_fin` se calcula automáticamente en `save()` sumando la duración del servicio.
# - `unique_together` evita duplicados para el mismo servicio y hora de inicio.
class Turno(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cliente_nombre = models.CharField(max_length=100)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(editable=False)
    confirmado = models.BooleanField(default=False)

    class Meta:
        ordering = ['fecha_hora_inicio']
        unique_together = ('servicio', 'fecha_hora_inicio')

    def __str__(self):
        return f"Turno para {self.cliente_nombre} - {self.servicio.nombre} el {self.fecha_hora_inicio.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        # Si no se ha establecido fecha_hora_fin, la calculamos automáticamente
        # usando la duración del servicio enlazado. Esto evita que el desarrollador
        # tenga que calcular y suministrar la hora de fin manualmente.
        if not self.fecha_hora_fin:
            # Asegurarse de que fecha_hora_inicio no sea None antes de sumar
            if self.fecha_hora_inicio:
                self.fecha_hora_fin = self.fecha_hora_inicio + timedelta(minutes=self.servicio.duracion_minutos)
        super().save(*args, **kwargs)


# Modelo Reserva: una alternativa simple para guardar reservas desde el
# formulario. En este proyecto conviven ambos conceptos (Turno y Reserva).
# - `Reserva` usa un campo `servicio` como CharField con choices por simplicidad.
# - `Turno` es más relacional y recomendable si quieres gestionar servicios
#   y turnos en detalle.
class Reserva(models.Model):
    # Opciones de servicios (valor/etiqueta)
    SERVICIO_CHOICES = [
        ('Unas', 'Uñas'),
        ('Corte_Pelo', 'Corte de Pelo'),
        ('Tintura', 'Tintura'),
    ]

    servicio = models.CharField(
        max_length=50,
        choices=SERVICIO_CHOICES,
        default='Corte_Pelo',
        verbose_name='Servicio'
    )

    # Otros campos de la reserva
    nombre_cliente = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(verbose_name='Fecha y Hora')

    def __str__(self):
        # Formato legible para administración y debugging
        return f"{self.servicio} - {self.nombre_cliente} ({self.fecha_hora.strftime('%d/%m %H:%M')})"