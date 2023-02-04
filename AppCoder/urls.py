from django.urls import path
from AppCoder.views import *


urlpatterns = [ 
    path("main/", inicio, name = "Start"), 

    # Atletas
    path("listaAtletas/", verAtletas, name = "Ver Atletas"), # Todos los Atletas
    path("crearAtletas/", crearAtletas, name="Crear Atletas"), # Crear Atleta
    path("buscarAtleta/", buscarAtleta, name="Buscar Estudiantes"), # Buscar Atletas
    path("verAtleta/", verAtleta), # Ver un Atleta

    # Wod
    path("listaWods/", verWods, name = "Ver Wods"), # Todos los Wod
    path("crearWods/", crearWods, name="Crear Wod"), # Crear Wod
    path("buscarWod/", buscarWod, name="Buscar Wod"), # Buscar Wod
    path("verWod/", verWod), # Ver un Wod
    path("value_list/", formulario_principal_view), # Ver un Wod
 
    # Movimientos
    path("listaMovimientos/", verMovimientos, name = "Ver Movimientos"), # Todos los Movimientos
    path("crearMovimientos/", crearMovimientos, name="Crear Movimientos"), # Crear Movimiento
    path("buscarMovimiento/", buscarMovimiento, name="Buscar Movimientos"), # Buscar Movimiento
    path("verMovimiento/", verMovimiento), # Ver un Movimiento

    # Score
    path("crearScore/", crearScore, name="Crear Score"), # Crear Movimiento


]
