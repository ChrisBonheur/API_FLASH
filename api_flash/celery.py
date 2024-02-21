"""from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Définir les paramètres de Django pour l'utilisation de Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_flash.settings')

# Créer une instance de l'application Celery
app = Celery('api_flash')

# Charger la configuration de Celery depuis les paramètres de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-découverte des tâches dans les applications Django
app.autodiscover_tasks()
"""
