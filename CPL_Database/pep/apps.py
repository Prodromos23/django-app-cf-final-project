from django.apps import AppConfig


class PepConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pep'

    def ready(self):
        import pep.signal_handler  # Ensure this line imports the signals