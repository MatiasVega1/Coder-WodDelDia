from django.db import models
from django.contrib.auth.models import User 
from django.db.models import Sum
from AppCoder.constants import *

# Cada atleta forma parte de un box
class Box(models.Model): 
    # Sólo necesito el nombre y la ubicación
    # No usé la ubicación en esta versión de la aplicación
    nombre = models.CharField(max_length=300) 
    ubicacion = models.CharField(max_length=300) 

class Atleta(models.Model):
    # Un atleta es aquel que realiza nuestras rutinas
    # Siempre es un usuario de nuestra web
    usuario = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    nombre= models.CharField(max_length=30)
    apellido= models.CharField(max_length=30) 
    edad = models.IntegerField()
    email = models.EmailField()
    # Datos del box
    box = models.ForeignKey(Box, related_name='box', on_delete=models.CASCADE, blank=True, default= None)

    # Encontre esta manera de hacer un campo de selección 
    nacionalidad = models.CharField(
        max_length=10,
        choices= NACIONALIDAD,
        default='ARG',
    ) 

    # Muestro los datos del Atleta
    def __str__(self):
        return self.apellido + ', ' + self.nombre
    # Obtengo el score de un atleta
    def getScoreAtleta(self):
        score = Score.objects.filter(atleta=self).aggregate(Sum('score'))['score__sum']
        return score or 0
    # Obtengo el avatar de un atleta
    # La relación es Atleta - Usuario - AvatarImagen
    def getAvatar(self):
        avatar = AvatarImagen.objects.filter(usuario=self.usuario).first()
        if avatar:
            return avatar.imagen
        else:
            return "avatarSinAvatar.jpg"    
    # Función que permite obtener un score de un wod puntual
    def getScoreWod(self, wod):
        score = Score.objects.filter(atleta=self, wod=wod).aggregate(Sum('score'))['score__sum']
        return score or 0

class Movimiento(models.Model):
    # Los movimientos son los que conforman el wod
    nombre= models.CharField(max_length=30)
    descripcion= models.CharField(max_length=1000)
    explicacion= models.CharField(max_length=200)
    imagen = models.ImageField(upload_to="movimientos", null=True, blank=True)

    # Encontre esta manera de hacer un campo de selección 
    dificultad = models.CharField(
        max_length=10,
        choices= VARIABLES,
        default='normal',
    )

    def __str__(self):
        return self.nombre.upper() + ": " + self.descripcion 

class Adaptacion(models.Model):
    # Los movimientos son los que conforman el wod
    movimiento = models.ForeignKey(Movimiento, related_name='movimiento', on_delete=models.CASCADE, blank=True, default= None)
    nombre= models.CharField(max_length=30)
    descripcion= models.CharField(max_length=1000)
    explicacion= models.CharField(max_length=200)

class Wod(models.Model):
    # Un wod es la rutina que debe ejecutar nuestro atleta, está conformada de movimientos
    nombre = models.CharField(max_length=40)
    duracion = models.IntegerField() 
 
    tipo = models.CharField(
        max_length=10,
        choices= TIPOS,
        default='TABATA',
    )  
    
    # Encontre esta manera de hacer un campo de selección 
    rondas = models.CharField(
        max_length=10,
        choices= RONDAS,
        default='Sin Rondas',
    )
    
    cantidad1 = models.IntegerField(blank=True, default=0)
    movimiento1 = models.ForeignKey(Movimiento, related_name='movimientos1', on_delete=models.CASCADE, blank=True, default= None)
    cantidad2 = models.IntegerField(null=True, blank=True, default=0)
    movimiento2 = models.ForeignKey(Movimiento, related_name='movimientos2', on_delete=models.CASCADE, null=True, blank=True, default= None)
    cantidad3 = models.IntegerField(blank=True, null=True, default=0)
    movimiento3 = models.ForeignKey(Movimiento, related_name='movimientos3', on_delete=models.CASCADE, null=True, blank=True, default= None)
    cantidad4 = models.IntegerField(blank=True, null=True, default=0)
    movimiento4 = models.ForeignKey(Movimiento, related_name='movimientos4', on_delete=models.CASCADE, null=True, blank=True, default= None)
    cantidad5 = models.IntegerField(blank=True, null=True, default=0)
    movimiento5 = models.ForeignKey(Movimiento, related_name='movimientos5', on_delete=models.CASCADE, null=True, blank=True, default= None)

    def __str__(self):
        return self.nombre.upper() + " (" + self.tipo + " " + str(self.duracion) + " min)"
    
    def getNombre(self):
        return self.nombre.upper()

class Score(models.Model):
    # El Score es el resultado que obtuvo el atleta a la hora de realizar el wod
    fecha = models.DateField()
    
    # Tengo que crear una FK a Wod y a Atleta ya que está relacionado a ambos
    wod = models.ForeignKey(Wod, on_delete=models.CASCADE)
    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self): 
        return  self.atleta.__str__() + " hizo el wod " + self.wod.__str__()  + " obeteniendo " + str(self.score) + " puntos (" + str(self.fecha)  +  ")"

class AvatarImagen(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    imagen = models.ImageField(upload_to="avatares", null=True, blank=True)

class Comentario(models.Model):
    # Cada usuario puede dejar un comentario en cualquier wod
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    wod = models.ForeignKey(Wod, on_delete = models.CASCADE) 
    titulo = models.CharField(max_length=300)  
    comentario = models.CharField(max_length=300) 
    fecha = models.CharField(max_length=300)

class Competencia(models.Model):
    # Una compentencia está conformada de tres wod
    nombre = models.CharField(max_length=300)   
    imagen = models.ImageField(upload_to="competencias", null=True, blank=True) 
    wod1 = models.ForeignKey(Wod, related_name='wod1',  on_delete = models.CASCADE)
    wod2 = models.ForeignKey(Wod, related_name='wod2',  on_delete = models.CASCADE)
    wod3 = models.ForeignKey(Wod, related_name='wod3', on_delete = models.CASCADE)

class ScoreCompetencia(models.Model):
    # Esto se usa para mostrar los resultados de cada competencia
    imagen = models.ImageField(upload_to="avatares", null=True, blank=True)
    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)
    wod1 = models.IntegerField()
    wod2 = models.IntegerField()
    wod3 = models.IntegerField()
    total = models.IntegerField() 