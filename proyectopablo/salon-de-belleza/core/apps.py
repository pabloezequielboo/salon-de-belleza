# Este archivo se utiliza para configurar la aplicación 'core'.
# Por ejemplo, puedes definir el nombre de la aplicación.

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
