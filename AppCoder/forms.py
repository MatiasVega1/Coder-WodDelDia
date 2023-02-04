from django import forms
from .models import *

# Acá utilizo Form porque me interesa hacerlo tal cual se realizó en clases
class AtletaFormulario(forms.Form):
    nombre= forms.CharField()
    apellido= forms.CharField()
    edad = forms.IntegerField()
    email = forms.EmailField()

# En estos casos, encontré más facilidad para crear los formularios a través de ModelForm
class WodFormulario(forms.ModelForm):
    class Meta:
        model = Wod
        fields = ['nombre','tipo','duracion']
    movimientos = forms.ModelChoiceField(queryset=Movimiento.objects.all())

class MovimientoFormulario(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['nombre','descripcion', 'dificultad']

class ScoreFormulario(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['fecha', 'score','wod','atleta'] 