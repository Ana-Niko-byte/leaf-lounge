from django.apps import AppConfig


class ReaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reader'

    def ready(self):
        """
        Imports the relevant signals.
        """
        import reader.signals
