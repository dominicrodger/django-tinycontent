from django.apps import AppConfig

from .conf import get_app_verbose_name


class TinyContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tinycontent'
    verbose_name = get_app_verbose_name()
