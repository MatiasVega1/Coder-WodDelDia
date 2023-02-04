from django.db import models



class Atleta(models.Model):
    nombre= models.CharField(max_length=30)
    apellido= models.CharField(max_length=30) 
    edad = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.apellido + ', ' + self.nombre

class Movimiento(models.Model):
    nombre= models.CharField(max_length=30)
    descripcion= models.CharField(max_length=200)

    VARIABLES = [
        ('facil', 'Facil'),
        ('normal', 'Normal'),
        ('dificil', 'Dificil'),
    ]
 
    dificultad = models.CharField(
        max_length=10,
        choices= VARIABLES,
        default='normal',
    )

    def __str__(self):
        return self.nombre.upper() + ": " + self.descripcion

# Create your models here.
class Wod(models.Model):
    nombre = models.CharField(max_length=40)

    TIPOS = [
        ('TABATA', 'TABATA'),
        ('EMOM', 'EMOM'),
        ('FOR TIME', 'FOR TIME'),
        ('AMRAP', 'AMRAP'),
    ]
 
    tipo = models.CharField(
        max_length=10,
        choices= TIPOS,
        default='TABATA',
    ) 
    duracion = models.IntegerField()
    movimientos = models.ForeignKey(Movimiento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre.upper() + " (" + self.tipo + " " + str(self.duracion) + " min)"


class Task(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=10)


class ValueList(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}: {self.value}"


class ValorSeleccionable(models.Model):
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}: {self.valor}"


class Dificultad(models.Model):
    DIFICULTAD_VARIABLES = [
        ('facil', 'Facil'),
        ('normal', 'Normal'),
        ('dificil', 'Dificil'),
    ]

    difficulty = models.CharField(
        max_length=10,
        choices= DIFICULTAD_VARIABLES,
        default='normal',
    )


class FormularioPrincipal(models.Model):
    nombre= models.CharField(max_length=30)
    descripcion= models.CharField(max_length=200)

    VARIABLES = [
        ('facil', 'Facil'),
        ('normal', 'Normal'),
        ('dificil', 'Dificil'),
    ]

    difficulty = models.CharField(
        max_length=10,
        choices= VARIABLES,
        default='normal',
    )


class Formulario(models.Model):
    VARIABLES = [
        ('facil', 'Facil'),
        ('normal', 'Normal'),
        ('dificil', 'Dificil'),
    ]

    difficulty = models.CharField(
        max_length=10,
        choices= VARIABLES,
        default='normal',
    )

class Score(models.Model):
    fecha = models.DateField()
    wod = models.ForeignKey(Wod, on_delete=models.CASCADE)
    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.atleta  + " hizo el wod " + self.wod + " en " + self.score + "(" + self.fecha +  ")"