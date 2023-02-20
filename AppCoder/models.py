from django.db import models
from django.contrib.auth.models import User 
from django import forms


# Creación de diccionarios para dificultad y para tipos de wod
# Podrían ser objetos pero a priori me interesaba probar con listas de valores predefinidos
# En versiones futuras pasarán probablemente a ser objetos

VARIABLES = [
        ('facil', 'Facil'),
        ('normal', 'Normal'),
        ('dificil', 'Dificil'),
    ]

TIPOS = [
        ('TABATA', 'TABATA'),
        ('EMOM', 'EMOM'),
        ('FOR TIME', 'FOR TIME'),
        ('AMRAP', 'AMRAP'),
    ]

RONDAS = [
        ('Sin Rondas', 'Sin Rondas'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'), 
        ('8', '8'), 
        ('9', '9'), 
        ('10', '10'), 
    ]

NACIONALIDAD = [
    ('ARG', 'Argentina'),
    ('BRA', 'Brasil'),
    ('COL', 'Colombia'),
    ('VEN', 'Venezuela'),
    ( 'PER', 'Perú'),
    ('BOL', 'Bolivia'),
    ('ECU', 'Ecuador'),
    ('CHI', 'Chile'),
    ( 'PAR', 'Paraguay'),
    ('URU', 'Uruguay')

]


class Box(models.Model): 
    nombre = models.CharField(max_length=300) 
    ubicacion = models.CharField(max_length=300) 

class Atleta(models.Model):
    # Un atleta es aquel que realiza nuestras rutinas
    usuario = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    nombre= models.CharField(max_length=30)
    apellido= models.CharField(max_length=30) 
    edad = models.IntegerField()
    email = models.EmailField()

     # Encontre esta manera de hacer un campo de selección 
    nacionalidad = models.CharField(
        max_length=10,
        choices= NACIONALIDAD,
        default='ARG',
    ) 

    box = models.ForeignKey(Box, related_name='box', on_delete=models.CASCADE, blank=True, default= None)


    def __str__(self):
        return self.apellido + ', ' + self.nombre

    def getNombre(self):
        todosLosScores = Score.objects.filter(atleta=self)
        score = 0 

        for sco in todosLosScores:
            score = score + sco.score
        return score
    
    def getScoreWod(self, wod):
        todosLosScores = Score.objects.filter(atleta=self)
        score = 0 

        for sco in todosLosScores:
            if (sco.wod == wod):
                score = score + sco.score
        return score
    


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

    # Hago el método getNombre para que, en caso que lo necesite, pueda solo mostrar el movimiento sin su explicacion
    def getNombre(self):
        return self.nombre

class Adaptacion(models.Model):
    # Los movimientos son los que conforman el wod
    movimiento = models.ForeignKey(Movimiento, related_name='movimiento', on_delete=models.CASCADE, blank=True, default= None)
    nombre= models.CharField(max_length=30)
    descripcion= models.CharField(max_length=1000)
    explicacion= models.CharField(max_length=200)


class Wod(models.Model):
    # Un wod es la rutina que debe ejecutar nuestro atleta, está conformada de movimientos
    nombre = models.CharField(max_length=40)
 
    tipo = models.CharField(
        max_length=10,
        choices= TIPOS,
        default='TABATA',
    ) 

    duracion = models.IntegerField() 

     # Encontre esta manera de hacer un campo de selección 
    rondas = models.CharField(
        max_length=10,
        choices= RONDAS,
        default='Sin Rondas',
    )
    cantidad1 = models.IntegerField(blank=True, default=0)
    movimiento1 = models.ForeignKey(Movimiento, related_name='movimientos1', on_delete=models.CASCADE, blank=True, default= None)
    cantidad2 = models.IntegerField(blank=True, default=0)
    movimiento2 = models.ForeignKey(Movimiento, related_name='movimientos2', on_delete=models.CASCADE, blank=True, default= None)
    cantidad3 = models.IntegerField(blank=True, default=0)
    movimiento3 = models.ForeignKey(Movimiento, related_name='movimientos3', on_delete=models.CASCADE, blank=True, default= None)
    cantidad4 = models.IntegerField(blank=True, default=0)
    movimiento4 = models.ForeignKey(Movimiento, related_name='movimientos4', on_delete=models.CASCADE, blank=True, default= None)
    cantidad5 = models.IntegerField(blank=True, default=0)
    movimiento5 = models.ForeignKey(Movimiento, related_name='movimientos5', on_delete=models.CASCADE, blank=True, default= None)

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
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    wod = models.ForeignKey(Wod, on_delete = models.CASCADE) 
    titulo = models.CharField(max_length=300)  
    comentario = models.CharField(max_length=300) 
    fecha = models.CharField(max_length=300)


class Competencia(models.Model):
    nombre = models.CharField(max_length=300)   
    imagen = models.ImageField(upload_to="competencias", null=True, blank=True) 
    wod1 = models.ForeignKey(Wod, related_name='wod1',  on_delete = models.CASCADE)
    wod2 = models.ForeignKey(Wod, related_name='wod2',  on_delete = models.CASCADE)
    wod3 = models.ForeignKey(Wod, related_name='wod3', on_delete = models.CASCADE)

class ScoreCompetencia(models.Model):
    imagen = models.ImageField(upload_to="avatares", null=True, blank=True)
    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)
    wod1 = models.IntegerField()
    wod2 = models.IntegerField()
    wod3 = models.IntegerField()
    total = models.IntegerField() 