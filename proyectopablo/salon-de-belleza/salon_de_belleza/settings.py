"""
Archivo de configuración de Django para el proyecto salon_de_belleza.

Para más información sobre este archivo, visita:
https://docs.djangoproject.com/en/stable/topics/settings/

Para la lista completa de configuraciones y sus valores, visita:
https://docs.djangoproject.com/en/stable/ref/settings/
"""

from pathlib import Path
import os

# Construye las rutas dentro del proyecto como: BASE_DIR / 'subdir'.
# BASE_DIR apunta al directorio raíz del proyecto Django (el que contiene manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Configuraciones de Seguridad ---

# ¡ADVERTENCIA DE SEGURIDAD: manten la clave secreta usada en producción en secreto!
# Esta clave se usa para la firma de datos criptográficos. Es vital que no se exponga.
# Para producción, es recomendable cargarla desde una variable de entorno o un gestor de secretos.
SECRET_KEY = 'django-insecure-a_dummy_secret_key_for_development'

# ¡ADVERTENCIA DE SEGURIDAD: no ejecutes con debug activado en producción!
# DEBUG = True activa los mensajes de error detallados en el navegador, lo cual es útil para desarrollar.
# En producción, debe ser False para no exponer información sensible de la configuración.
DEBUG = True

# ALLOWED_HOSTS define qué nombres de dominio o IPs pueden servir este sitio Django.
# En desarrollo, a menudo se deja vacío o con ['*'].
# En producción, debes listar aquí tu dominio o dominios, por ejemplo: ['www.misalon.com']
ALLOWED_HOSTS = []


# --- Definición de Aplicaciones ---

# INSTALLED_APPS es una lista de todas las aplicaciones que se usan en este proyecto Django.
# Django viene con varias aplicaciones por defecto que manejan tareas comunes.
# También aquí se registrarán las aplicaciones que tú crees.
INSTALLED_APPS = [
    'django.contrib.admin',         # El sitio de administración.
    'django.contrib.auth',          # El framework de autenticación.
    'django.contrib.contenttypes',  # El framework para tipos de contenido.
    'django.contrib.sessions',      # El framework de sesiones.
    'django.contrib.messages',      # El framework de mensajería.
    'django.contrib.staticfiles',   # El framework para manejar archivos estáticos.
    'core', # Aplicación principal del proyecto
]

# --- Middleware ---

# MIDDLEWARE es una lista de "ganchos" en el sistema de procesamiento de peticiones/respuestas de Django.
# Cada clase de middleware tiene una responsabilidad específica. El orden es importante.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# --- Configuración de URLs ---

# ROOT_URLCONF le dice a Django cuál es el módulo de Python que contiene la configuración de URLs principal.
# Normalmente, apunta al archivo `urls.py` del directorio de tu proyecto.
ROOT_URLCONF = 'salon_de_belleza.urls'


# --- Plantillas (Templates) ---

# TEMPLATES define cómo Django encontrará y renderizará las plantillas HTML.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIRS es una lista de directorios donde Django buscará plantillas.
        # Es común añadir un directorio 'templates' en la raíz del proyecto.
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True, # APP_DIRS=True le dice a Django que busque plantillas dentro de los directorios de las aplicaciones.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# --- Interfaz de Servidor de Aplicaciones Web (WSGI) ---

# WSGI_APPLICATION especifica la ruta al objeto de la aplicación WSGI que los servidores
# compatibles con WSGI usan para comunicarse con tu proyecto.
WSGI_APPLICATION = 'salon_de_belleza.wsgi.application'


# --- Base de Datos ---
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

# DATABASES configura la(s) base(s) de datos que usará tu proyecto.
# Por defecto, Django usa SQLite, que es una base de datos ligera basada en un solo archivo.
# Es ideal para desarrollo y proyectos pequeños.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --- Validación de Contraseñas ---
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS es una lista de validadores que se usan para comprobar
# la seguridad de las contraseñas de los usuarios.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# --- Internacionalización (i18n) y Localización (l10n) ---
# https://docs.djangoproject.com/en/stable/topics/i18n/

# LANGUAGE_CODE define el código de idioma por defecto para este proyecto.
LANGUAGE_CODE = 'es-ar' # Español de Argentina

# TIME_ZONE define la zona horaria por defecto.
TIME_ZONE = 'UTC'

# USE_I18N activa el sistema de traducción de Django.
USE_I18N = True

# USE_L10N activa el formato de números y fechas según la localización.
USE_L10N = True

# USE_TZ activa el soporte para zonas horarias. Cuando es True, Django almacena
# la fecha y hora en UTC en la base de datos.
USE_TZ = True


# --- Archivos Estáticos (CSS, JavaScript, Imágenes) ---
# https://docs.djangoproject.com/en/stable/howto/static-files/

# STATIC_URL es la URL base desde la cual se servirán los archivos estáticos.
# Por ejemplo, '/static/css/style.css'.
STATIC_URL = '/static/'

# STATICFILES_DIRS es una lista de directorios donde Django buscará archivos estáticos,
# además del directorio 'static/' de cada aplicación.
# Es común añadir un directorio 'static' en la raíz del proyecto.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# --- Campo de Clave Primaria por Defecto ---
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD define el tipo de campo que se usará para las claves primarias
# autoincrementales que Django crea por defecto.
# A partir de Django 3.2, se recomienda usar BigAutoField para evitar posibles problemas
# de desbordamiento en bases de datos grandes.

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Configuración de franjas horarias para reservas ---
# `RESERVATION_START_HOUR` y `RESERVATION_END_HOUR` definen el rango de horas
# para mostrar como posibles inicios de turno. `RESERVATION_END_HOUR` es
# exclusivo en el rango (por ejemplo, 9..18 genera 09:00..17:00).
RESERVATION_START_HOUR = 9
RESERVATION_END_HOUR = 18
# Duración por defecto de cada turno en minutos (por ejemplo 60 = 1 hora)
RESERVATION_SLOT_DURATION_MINUTES = 60
