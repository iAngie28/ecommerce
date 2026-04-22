from django.db import transaction
from abc import ABC

class BaseService(ABC):
    def __init__(self, model_class):
        self.model_class = model_class
    
    @transaction.atomic
    def crear(self, datos_validados):
        return self.model_class.objects.create(**datos_validados)
    
    @transaction.atomic
    def actualizar(self, instancia, datos_validados):
        for campo, valor in datos_validados.items():
            setattr(instancia, campo, valor)
        instancia.save()
        return instancia