from django.apps import AppConfig


class MigrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'migration'
    verbose_name = 'Data Migration'

    def ready(self):
        """Import signals when app is ready"""
        # Import signals here if needed
        pass
