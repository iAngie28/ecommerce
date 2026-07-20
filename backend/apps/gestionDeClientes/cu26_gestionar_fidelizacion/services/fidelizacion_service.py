from django.db import transaction
from django.core.exceptions import ValidationError
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.models.cuenta_puntos import CuentaPuntos
from apps.gestionDeClientes.cu26_gestionar_fidelizacion.models.historial_puntos import HistorialPuntos
from apps.gestionDeVentasYFacturacion.cu13_gestionar_estado_de_pedido.models.pedido import Pedido

class FidelizacionService:
    # Reglas de negocio configurables en el futuro, por ahora hardcodeadas
    PUNTOS_POR_BS = 0.1  # Ejemplo: 10 Bs = 1 Punto
    VALOR_BS_POR_PUNTO = 0.05  # Ejemplo: 100 Puntos = 5 Bs de descuento

    @staticmethod
    def obtener_o_crear_cuenta(cliente_id) -> CuentaPuntos:
        cuenta, created = CuentaPuntos.objects.get_or_create(cliente_id=cliente_id)
        return cuenta

    @staticmethod
    @transaction.atomic
    def acumular_puntos_por_compra(pedido_id):
        """
        Calcula los puntos basados en el total del pedido y los suma a la cuenta.
        Se usa `select_for_update` para evitar condiciones de carrera (Race Conditions).
        """
        try:
            pedido = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            return

        # Calcular puntos (redondeo hacia abajo)
        puntos_a_sumar = int(float(pedido.total) * FidelizacionService.PUNTOS_POR_BS)
        
        if puntos_a_sumar <= 0:
            return

        # Bloquear fila de la cuenta para actualización segura
        cuenta = CuentaPuntos.objects.select_for_update().get_or_create(cliente_id=pedido.cliente_id)[0]
        
        # Actualizar saldos
        cuenta.saldo_actual += puntos_a_sumar
        cuenta.puntos_historicos += puntos_a_sumar
        cuenta.save()
        
        # Registrar historial
        HistorialPuntos.objects.create(
            cuenta=cuenta,
            tipo_operacion='ACUMULACION',
            monto_puntos=puntos_a_sumar,
            referencia=f"Pedido #{pedido.id}"
        )

    @staticmethod
    @transaction.atomic
    def canjear_puntos(cliente_id, puntos_a_canjear: int, referencia: str) -> float:
        """
        Descuenta los puntos de la cuenta y retorna el valor en Bs de descuento.
        Levanta ValidationError si no hay suficientes puntos.
        """
        if puntos_a_canjear <= 0:
            raise ValidationError("La cantidad de puntos a canjear debe ser mayor a 0.")

        cuenta = CuentaPuntos.objects.select_for_update().get(cliente_id=cliente_id)
        
        if cuenta.saldo_actual < puntos_a_canjear:
            raise ValidationError(f"Saldo insuficiente. Tienes {cuenta.saldo_actual} puntos.")

        cuenta.saldo_actual -= puntos_a_canjear
        cuenta.save()
        
        HistorialPuntos.objects.create(
            cuenta=cuenta,
            tipo_operacion='CANJE',
            monto_puntos=-puntos_a_canjear,
            referencia=referencia
        )
        
        # Retornar el valor equivalente en descuento
        return puntos_a_canjear * FidelizacionService.VALOR_BS_POR_PUNTO
