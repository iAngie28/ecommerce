from django.apps import AppConfig


class Cu25Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist'
    label = 'cu25_gestionar_wishlist'

    def ready(self):
        import apps.gestionDeVentasYFacturacion.cu25_gestionar_wishlist.signals  # noqa: F401
