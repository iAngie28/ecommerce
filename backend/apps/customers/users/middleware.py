import logging

logger = logging.getLogger(__name__)

class TenantHostMiddleware:
    """
    Middleware para limpiar el host de puertos y espacios antes de que 
    django-tenants intente identificar al inquilino (tenant).
    
    Esto permite que:
    1. En local funcione http://tienda1.localhost:8001 (limpia el :8001)
    2. En Nginx funcione correctamente con o sin puertos.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request.get_host() devuelve 'nombre:puerto'
        original_host = request.get_host()
        parts = original_host.split(':')
        host = parts[0].lower().strip()
        port_suffix = f":{parts[1].strip()}" if len(parts) > 1 else ""

        # Guardamos el host original por si acaso
        request.original_host = original_host

        # Log para depuración: host y cabeceras relevantes
        try:
            logger.warning(f"TenantHostMiddleware - original_host={request.original_host} | computed_host={host} | HTTP_HOST_before={request.META.get('HTTP_HOST')}")
            # Print explícito para asegurar salida en consola de desarrollo
            pass
        except Exception:
            pass

        # Forzamos que Django vea el host limpio PERO con su puerto,
        # para que DRF genere URLs absolutas correctas (ej: /media/...).
        # django-tenants internamente ya quita el puerto para buscar el Tenant.
        request.META['HTTP_HOST'] = f"{host}{port_suffix}"

        return self.get_response(request)
