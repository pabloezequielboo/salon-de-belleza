#!/usr/bin/env python
"""
Utilidad de línea de comandos de Django para tareas administrativas.

Este script es el equivalente de `django-admin` pero específico para tu proyecto.
Se utiliza para ejecutar comandos de administración como:
- `runserver`: Iniciar el servidor de desarrollo.
- `makemigrations`: Crear nuevas migraciones basadas en los cambios de tus modelos.
- `migrate`: Aplicar las migraciones a la base de datos.
- `startapp`: Crear una nueva aplicación dentro del proyecto.
- `collectstatic`: Recolectar archivos estáticos en un solo lugar.
- Y muchos más.
"""
import os
import sys


def main():
    """
    Función principal que se encarga de la configuración y ejecución de tareas.
    """
    # La siguiente línea es crucial. Le dice a Django dónde encontrar la configuración de tu proyecto.
    # 'DJANGO_SETTINGS_MODULE' es una variable de entorno que Django utiliza para localizar el archivo `settings.py`.
    # 'salon_de_belleza.settings' significa: busca un paquete llamado `salon_de_belleza` y dentro de él, un módulo llamado `settings`.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_de_belleza.settings')
    try:
        # Se importa la función `execute_from_command_line` que es el corazón de la funcionalidad de `manage.py`.
        # Esta función se encarga de procesar los argumentos de la línea de comandos y ejecutar la tarea correspondiente.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si la importación de Django falla, se lanza un error descriptivo.
        # Esto suele ocurrir por dos razones comunes:
        # 1. Django no está instalado en el entorno de Python que se está utilizando.
        # 2. Se está utilizando un entorno virtual (`venv`) y no ha sido activado.
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado y "
            "disponible en tu variable de entorno PYTHONPATH? ¿Olvidaste "
            "activar un entorno virtual?"
        ) from exc
    # `sys.argv` es una lista que contiene los argumentos pasados al script desde la línea de comandos.
    # Por ejemplo, si ejecutas `python manage.py runserver 8080`, `sys.argv` será `['manage.py', 'runserver', '8080']`.
    # `execute_from_command_line` utiliza estos argumentos para realizar la acción solicitada.
    execute_from_command_line(sys.argv)


# `__name__ == '__main__'` es una construcción estándar en Python.
# Significa que el código dentro de este bloque solo se ejecutará cuando el script
# sea ejecutado directamente desde la línea de comandos, y no cuando sea importado por otro script.
if __name__ == '__main__':
    main()