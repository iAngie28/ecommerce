from django import forms
from .models import DatoProyecto # El "." indica que busque en la misma carpeta

class DatoProyectoForm(forms.ModelForm):
    class Meta:
        model = DatoProyecto
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Inventario Marzo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }