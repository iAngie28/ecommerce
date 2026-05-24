from django.apps import AppConfig


class AppNegocioConfig(AppConfig):
    name = 'apps.negocio'
    label = 'app_negocio'

    def ready(self):
        import apps.negocio.notificaciones.signals
