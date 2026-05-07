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
        host = request.get_host().split(':')[0].lower().strip()

        # Guardamos el host original por si acaso
        request.original_host = request.get_host()

        # Log para depuración: host y cabeceras relevantes
        try:
            logger.warning(f"TenantHostMiddleware - original_host={request.original_host} | computed_host={host} | HTTP_HOST_before={request.META.get('HTTP_HOST')}")
            # Print explícito para asegurar salida en consola de desarrollo
            print(f"[TenantHostMiddleware] original_host={request.original_host} computed_host={host} HTTP_HOST_before={request.META.get('HTTP_HOST')}")
        except Exception:
            pass

        # Forzamos que Django vea el host sin puerto en la cabecera HTTP_HOST
        # Solo para el procesamiento interno de este request.
        request.META['HTTP_HOST'] = host

        return self.get_response(request)
