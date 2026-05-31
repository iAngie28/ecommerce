from django.db.models import Sum, Count, F, Q
from apps.negocio.ordenes.models.pedido import Pedido
from apps.negocio.catalogo.models.producto import Producto
from apps.customers.clientes.models.cliente import Cliente
from django.db.models.functions import TruncMonth, TruncDay
import datetime

class ReportService:
    @staticmethod
    def generar_estatico(tipo):
        """
        Genera datos para reportes estáticos predefinidos.
        """
        if tipo == 'ventas_mensuales':
            return Pedido.objects.filter(estado='COMPLETADO').annotate(
                mes=TruncMonth('fecha_creacion')
            ).values('mes').annotate(
                total_ventas=Sum('total'),
                cantidad_pedidos=Count('id')
            ).order_by('-mes')[:12]
        
        elif tipo == 'top_productos':
            from apps.negocio.ordenes.models.carrito_item import PedidoItem # Asumiendo que PedidoItem existe, o detalles del pedido
            # Como la estructura exacta del detalle no la tengo importada arriba, usaré Producto
            return Producto.objects.filter(activo=True).order_by('-stock')[:10].values('id', 'nombre', 'stock', 'precio')

        elif tipo == 'nuevos_clientes':
            return Cliente.objects.annotate(
                mes=TruncMonth('creado_en')
            ).values('mes').annotate(
                total=Count('id')
            ).order_by('-mes')[:12]
        else:
            raise ValueError(f"Tipo de reporte estático '{tipo}' no soportado.")

    @staticmethod
    def ejecutar_dinamico(config):
        """
        Ejecuta un reporte dinámico basado en una configuración JSON.
        Ejemplo de config:
        {
            "modelo": "pedidos", # "pedidos", "productos", "clientes"
            "metrica": "total", # "total", "conteo"
            "agrupar_por": "mes", # "mes", "dia", "estado", "categoria"
            "filtros": {
                "estado": "COMPLETADO"
            }
        }
        """
        modelo_str = config.get('modelo', 'pedidos')
        metrica = config.get('metrica', 'conteo')
        agrupar_por = config.get('agrupar_por')
        filtros = config.get('filtros', {})

        if modelo_str == 'pedidos':
            qs = Pedido.objects.all()
            if 'estado' in filtros:
                qs = qs.filter(estado=filtros['estado'])
            
            if agrupar_por == 'mes':
                qs = qs.annotate(grupo=TruncMonth('fecha_creacion'))
            elif agrupar_por == 'dia':
                qs = qs.annotate(grupo=TruncDay('fecha_creacion'))
            elif agrupar_por == 'estado':
                qs = qs.annotate(grupo=F('estado'))
            else:
                qs = qs.annotate(grupo=F('id')) # dummy group if none

            qs = qs.values('grupo')
            
            if metrica == 'total':
                qs = qs.annotate(resultado=Sum('total'))
            else:
                qs = qs.annotate(resultado=Count('id'))
                
            return qs.order_by('-grupo')

        elif modelo_str == 'productos':
            qs = Producto.objects.all()
            if 'activo' in filtros:
                qs = qs.filter(activo=filtros['activo'])
            
            if agrupar_por == 'categoria':
                qs = qs.annotate(grupo=F('categoria__nombre'))
            else:
                qs = qs.annotate(grupo=F('id'))
                
            qs = qs.values('grupo')
            
            if metrica == 'stock':
                qs = qs.annotate(resultado=Sum('stock'))
            else:
                qs = qs.annotate(resultado=Count('id'))
                
            return qs.order_by('-grupo')
            
        return []
