from django.db import transaction
from django.core.exceptions import ValidationError
from apps.core.services import BaseService
from apps.gestionDeProductoYCatalogo.cu24_gestionar_reseñas.models.reseña import Reseña
from apps.gestionDeVentasYFacturacion.cu14_generar_facturacion.models.detalle_factura import DetalleFactura
from apps.gestionDeReportes.cu18_gestionar_notificaciones.models.notificacion import Notificacion
from apps.gestionDeUsuarioySeguridad.cu6_gestionar_bitacora.services.bitacora_service import BitacoraService

class ReseñaService(BaseService):
    def __init__(self):
        super().__init__(model_class=Reseña)

    def get_model(self):
        return Reseña

    def puede_reseñar(self, cliente_id, producto_id) -> bool:
        """
        Verifica si el cliente ha comprado el producto.
        Busca en DetalleFactura donde la factura esté en estado VIGENTE.
        """
        return DetalleFactura.objects.filter(
            factura__cliente_id=cliente_id,
            factura__estado='VIGENTE',
            producto_id=producto_id
        ).exists()

    @transaction.atomic
    def crear_reseña(self, cliente_id, producto_id, calificacion, comentario=None):
        if not self.puede_reseñar(cliente_id, producto_id):
            raise ValidationError("Solo puedes reseñar productos que hayas comprado.")
        
        if Reseña.objects.filter(cliente_id=cliente_id, producto_id=producto_id).exists():
            raise ValidationError("Ya has escrito una reseña para este producto.")
            
        reseña = Reseña.objects.create(
            cliente_id=cliente_id,
            producto_id=producto_id,
            calificacion=calificacion,
            comentario=comentario,
            estado='APROBADA'
        )
        
        # Notificar a los administradores
        Notificacion.objects.create(
            # Idealmente se envía a los usuarios ADMIN o al VENDEDOR de la tienda.
            # En este caso, lo marcamos de tipo SISTEMA, 
            # asumiendo que el frontend administrativo las leerá si tipo='SISTEMA' o destinadas a admin.
            titulo="Nueva Reseña Publicada",
            mensaje=f"Se ha recibido y publicado automáticamente una nueva reseña de {calificacion} estrellas para el producto ID {producto_id}.",
            tipo='SISTEMA'
        )
        
        return reseña

    def calcular_promedio(self, producto_id) -> dict:
        reseñas_aprobadas = Reseña.objects.filter(producto_id=producto_id, estado='APROBADA')
        total = reseñas_aprobadas.count()
        if total == 0:
            return {'promedio': 0, 'total_reseñas': 0}
            
        suma = sum([r.calificacion for r in reseñas_aprobadas])
        return {
            'promedio': round(suma / total, 1),
            'total_reseñas': total
        }

    @transaction.atomic
    def cambiar_estado(self, reseña_id, nuevo_estado, usuario):
        if nuevo_estado not in ['APROBADA', 'RECHAZADA']:
            raise ValidationError("Estado inválido.")
            
        reseña = self.get_by_id(reseña_id)
        if not reseña:
            raise ValidationError("La reseña no existe.")
            
        estado_anterior = reseña.estado
        reseña.estado = nuevo_estado
        reseña.save(update_fields=['estado'])
        
        BitacoraService.registrar_accion(
            usuario=usuario,
            accion="MODERACION_RESEÑA",
            detalles=f"Reseña ID {reseña_id} cambió de {estado_anterior} a {nuevo_estado}"
        )
        
        return reseña
