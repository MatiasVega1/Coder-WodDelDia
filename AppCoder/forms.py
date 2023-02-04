from django import forms

from .models import Task
from .models import ValueList
from .models import ValorSeleccionable

from .models import Dificultad
from .models import FormularioPrincipal, Formulario, Movimiento, Wod, Score, Atleta

class AtletaFormulario(forms.Form):
    nombre= forms.CharField()
    apellido= forms.CharField()
    edad = forms.IntegerField()
    email = forms.EmailField()


class FormularioForm(forms.ModelForm):
    class Meta:
        model = Dificultad
        fields = ['difficulty']



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
        fields = ['fecha', 'score']
    wods = forms.ModelChoiceField(queryset=Wod.objects.all())
    atletas = forms.ModelChoiceField(queryset=Atleta.objects.all())


class TaskForm(forms.ModelForm):
     class Meta:
        model = Task
        fields = ['name', 'status']

        
class ValueListForm(forms.ModelForm):
    list = ('a','b')
  #  valor_seleccionable = forms.ModelChoiceField(queryset= list.all(), empty_label=None)
    dificultad = forms.CharField()


class FormularioPrincipalForm(forms.ModelForm):
    class Meta:
        model = FormularioPrincipal
        fields = ['nombre','descripcion', 'difficulty']

class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ['difficulty']