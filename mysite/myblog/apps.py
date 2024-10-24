from django.apps import AppConfig


class MyblogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myblog'

    def ready(self):
        from .signals import create_profile, save_profile