from django.apps import AppConfig


class AuditappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auditApp'

    def ready(self):
        import auditApp.signals
