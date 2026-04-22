from core.views import BaseViewSet
from customers.models import Plan
from customers.serializers.plan_serializer import PlanSerializer
from customers.services.plan_service import PlanService


class PlanViewSet(BaseViewSet):
    """
    API de Planes de Suscripción.
    
    - GET /api/planes/ - Listar todos
    - POST /api/planes/ - Crear nuevo
    - GET /api/planes/{id}/ - Detalle
    - PUT /api/planes/{id}/ - Actualizar
    - DELETE /api/planes/{id}/ - Eliminar
    """
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    modulo_auditoria = "Plan"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = PlanService()
