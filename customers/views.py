from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer # Importas el de arriba

class MyTokenObtainPairView(TokenObtainPairView):
    # Esto le dice a la vista que use TU lógica y no la de defecto
    serializer_class = MyTokenObtainPairSerializer