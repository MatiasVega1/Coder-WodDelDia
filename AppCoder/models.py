from django.db import models

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

class Atleta(models.Model):
    # Un atleta es aquel que realiza nuestras rutinas
    nombre= models.CharField(max_length=30)
    apellido= models.CharField(max_length=30) 
    edad = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.apellido + ', ' + self.nombre

class Movimiento(models.Model):
    # Los movimientos son los que conforman el wod
    nombre= models.CharField(max_length=30)
    descripcion= models.CharField(max_length=200)

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

class Wod(models.Model):
    # Un wod es la rutina que debe ejecutar nuestro atleta, está conformada de movimientos
    nombre = models.CharField(max_length=40)
 
    tipo = models.CharField(
        max_length=10,
        choices= TIPOS,
        default='TABATA',
    ) 

    duracion = models.IntegerField()
    movimientos = models.ForeignKey(Movimiento, on_delete=models.CASCADE)

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