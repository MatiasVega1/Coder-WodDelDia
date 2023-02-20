from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User



# Acá utilizo Form porque me interesa hacerlo tal cual se realizó en clases
class AtletaFormulario(forms.ModelForm):   
    class Meta:
        model = Atleta
        fields = ['nombre','apellido','edad', 'email', 'box','nacionalidad']

# En estos casos, encontré más facilidad para crear los formularios a través de ModelForm
class WodFormulario(forms.ModelForm):
    class Meta:
        model = Wod
        fields = ['nombre','tipo','duracion', 'rondas']
    cantidad1 = forms.IntegerField()
    movimiento1 = forms.ModelChoiceField(queryset=Movimiento.objects.all())
    cantidad2 = forms.IntegerField()
    movimiento2 = forms.ModelChoiceField(queryset=Movimiento.objects.all())
    cantidad3 = forms.IntegerField()
    movimiento3 = forms.ModelChoiceField(queryset=Movimiento.objects.all())
    cantidad4 = forms.IntegerField()
    movimiento4 = forms.ModelChoiceField(queryset=Movimiento.objects.all())
    cantidad5 = forms.IntegerField()
    movimiento5 = forms.ModelChoiceField(queryset=Movimiento.objects.all())

class MovimientoFormulario(forms.ModelForm):
    explicacion = forms.URLField(label='URL del enlace')
    class Meta:
        model = Movimiento
        fields = ['nombre','descripcion', 'dificultad', 'imagen'] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update({'accept': 'image/*'})

class ScoreFormulario(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['fecha', 'score','atleta'] 

class RegistroFormulario(UserCreationForm):
    first_name = forms.CharField(label = "Nombre")
    last_name = forms.CharField(label = "Apellido")
    email = forms.EmailField(label = "Correo")

    password1 = forms.CharField(label = "Ingrese un password:", widget = forms.PasswordInput)
    password2 = forms.CharField(label = "Repita el password:", widget = forms.PasswordInput)
    
    class Meta: 
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class AvatarImagenFormulario(forms.ModelForm):
    class Meta:
        model = AvatarImagen
        fields = ['imagen'] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update({'accept': 'image/*'})


class ComentarioFormulario(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario'] 

class AdaptacionFormulario(forms.ModelForm):
    class Meta:
        model = Adaptacion
        fields = ['nombre', 'descripcion', 'explicacion' ] 

class CompetenciaFormulario(forms.ModelForm):
    wod1 = forms.ModelChoiceField(queryset=Wod.objects.all())
    wod2 = forms.ModelChoiceField(queryset=Wod.objects.all())
    wod3 = forms.ModelChoiceField(queryset=Wod.objects.all())
    
    class Meta:
        model = Competencia
        fields = ['nombre','imagen' ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update({'accept': 'image/*'})