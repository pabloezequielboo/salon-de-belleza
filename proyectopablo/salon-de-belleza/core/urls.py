from django.urls import path
from . import views

# Rutas específicas de la app 'core'. Se incluyen desde el archivo
# de URLs principal del proyecto (`salon_de_belleza/urls.py`).
urlpatterns = [
    # Página principal
    path('', views.index, name='index'),

    # Muestra el formulario y procesa el POST para crear una reserva
    path('reservar/', views.reservar_turno_view, name='crear_reserva'),

    # Página de servicios
    path('servicios/', views.servicios_view, name='servicios'),

    # Página de confirmación tras crear la reserva
    path('reserva-exitosa/', views.reserva_exitosa_view, name='reserva_exitosa'),

    # Página de contacto
    path('contacto/', views.contacto_view, name='contacto'),
]