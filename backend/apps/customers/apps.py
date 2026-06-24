from django.apps import AppConfig


class CustomersConfig(AppConfig):
    name = 'apps.customers'
    label = 'customers'

    def ready(self):
        import os
        # Evitar arrancar el scheduler en workers o comandos (como makemigrations)
        if os.environ.get('RUN_MAIN', None) == 'true':
            try:
                from apps.gestionDeReportes.cu21_generar_backup.services.scheduler import start_scheduler
                start_scheduler()
            except ImportError as e:
                print(f"Error importando scheduler: {e}")
                
        # Registrar señales de tenants (límites de plan, etc)
        try:
            import apps.customers.tenants.signals
        except ImportError:
            pass
