from django.apps import AppConfig

class Cu26Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gestionDeClientes.cu26_gestionar_fidelizacion'
    label = 'cu26_gestionar_fidelizacion'
    verbose_name = 'Programa de Fidelización'

    def ready(self):
        # Importa los signals cuando la app esté lista
        import apps.gestionDeClientes.cu26_gestionar_fidelizacion.signals
