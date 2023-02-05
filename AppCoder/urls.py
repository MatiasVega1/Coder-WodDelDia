from django.urls import path
from AppCoder.views import *


urlpatterns = [ 
    path("", inicio), 
    path("main/", inicio, name = "Start"), 

    # Atletas
    path("listaAtletas/", verAtletas, name = "Ver Atletas"), # Todos los Atletas
    path("crearAtletas/", crearAtletas, name="Crear Atletas"), # Crear Atleta 
    path("verAtleta/", verAtleta, name="Filtrar Atleta"), # Ver un Atleta

    # Wod
    path("listaWods/", verWods, name = "Ver Wods"), # Todos los Wod
    path("crearWods/", crearWods, name="Crear Wod"), # Crear Wod 
    path("verWod/", verWod, name="Filtrar Wod"), # Ver un Wod 
 
    # Movimientos
    path("listaMovimientos/", verMovimientos, name = "Ver Movimientos"), # Todos los Movimientos
    path("crearMovimientos/", crearMovimientos, name="Crear Movimientos"), # Crear Movimiento 
    path("verMovimiento/", verMovimiento, name="Filtrar Movimiento"), # Ver un Movimiento

    # Score
    path("crearScore/", crearScore, name="Crear Score"), # Crear Score
    path("listaScore/", verScore, name = "Ver Scores"), # Todos los Scores
    path("listaScoreFiltro/", verScore, name = "Ver Scores Filtrados"), # Todos los Scores filtrados
 


]
