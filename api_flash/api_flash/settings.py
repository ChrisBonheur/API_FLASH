from pathlib import Path
from .constantes import YEAR_ID_HEADER
from datetime import timedelta
import os
from datetime import timedelta, datetime
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'fr'
ADMIN_LANGUAGE_CODE = 'fr'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "lOz|u5AhmYTtD:5Ni?tLDW&#VA{fP1%olmB{x}tvCC-]Zq)w"

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost',
    "test-umng-flash.zandosoft.online", 
    "umng-flash.zandosoft.online", 
    "test-api-flash.zandosoft.online",
    "api-flash.zandosoft.online",
    '206.189.238.182',
    '*'
]

#SECURE_HSTS_SECONDS = 31536000
#SESSION_COOKIE_SECURE = True
#SECURE_SSL_REDIRECT = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_yasg",
    "agent",
    "config_global",
    "corsheaders",
    "academic_years",
    "reporting",
    "teacher",
    "review",
    "student"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "api_flash.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api_flash.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "dbtouseformysql.sqlite3",
    }
}

"""
DATABASES = {  
    'default': {  
        'ENGINE':  'django.db.backends.mysql',  
        'NAME': 'c2418006c_flash',
        'USER': 'c2418006c_bonheur',
        'PASSWORD': 'vKrpq}2>ZQiwrnT',
        'HOST': 'localhost',  
        'PORT': '3306',  
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

#Authorized link
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']

LANGUAGE_CODE = "fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#Send email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.umng-flash.com'  # Adresse du serveur SMTP
EMAIL_PORT = 587  # Port du serveur SMTP
EMAIL_USE_TLS = True  # Utilisation de TLS pour sécuriser la connexion SMTP

# Si votre serveur SMTP nécessite une authentification
EMAIL_HOST_USER = 'flash@umng-flash.com'  # Votre adresse e-mail
EMAIL_HOST_PASSWORD = "e@f25Bc76"  # Votre mot de passe


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'custom_header': {  # Définition de votre en-tête personnalisé
            'type': 'apiKey',
            'name': 'academic_year_id',  # Nom de l'en-tête personnalisé
            'in': 'header'
        }
    },
}

now = datetime.now()

# Calculer la durée jusqu'à minuit
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
time_until_midnight = midnight - now

# Définir ACCESS_TOKEN_LIFETIME sur la durée jusqu'à minuit
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',)
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',  # Nom de la table qui sera utilisée pour le cache
        'TIMEOUT': 604800,  # Durée de vie en secondes (300s = 5 minutes)
        'OPTIONS': {
            'MAX_ENTRIES': 1000,  # Nombre maximum d'entrées dans la table de cache
            'CULL_FREQUENCY': 3,  # Proportion des entrées purgées quand le cache atteint sa taille maximale
        },
    }
}
