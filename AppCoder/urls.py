from django.urls import path
from AppCoder.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [ 
    path("", inicio), 
    path("main/", inicio, name = "Start"), 

    # Autentiación
    path("registro/", registro, name="Sign Up"),
    path("login/", iniciarSesion, name="Log In"),
    path("logout/", LogoutView.as_view(template_name = "AppCoder/logout.html"), name="Log Out"),


    # Atletas
    path("listaAtletas/", verAtletas, name = "Ver Atletas"), # Todos los Atletas
    path("crearAtletas/", crearAtletas, name="Crear Atletas"), # Crear Atleta 
    path("verAtleta/", verAtleta, name="Filtrar Atleta"), # Ver un Atleta
    

    path("listaAtletasLista/", AtletaLista.as_view(), name = "Ver Atletas Lista"), # Todos los Atletas
    path("atleta/nuevo/", AtletaCrear.as_view(), name = "Crear Atleta"),
    path("atleta/borrar/<int:pk>", AtletaBorrar.as_view(), name = "Borrar Atleta"),
    path("ateta/editar/<int:pk>", AtletaEditar.as_view(), name = "Editar Atleta"),

    # Wod
    path("listaWods/", verWods, name = "Ver Wods"), # Todos los Wod
    path("crearWods/", crearWods, name="Crear Wod"), # Crear Wod 
    path("verWod/<wod_nombre>", verWod, name="Filtrar Wod"), # Ver un Wod 
    path("filtrarWod/", filtrarWod, name="Filtrar Wod Tipo"), # Ver un Wod 
 
    # Movimientos
    path("listaMovimientos/", verMovimientos, name = "Ver Movimientos"), # Todos los Movimientos
    path("crearMovimientos/", crearMovimientos, name="Crear Movimientos"), # Crear Movimiento 
    path("verMovimiento/<movimiento_nombre>", verMovimiento, name="Filtrar Movimiento"), # Ver un Movimiento
    path("filtrarMovimiento/", filtrarMovimiento, name="Filtrar Movimiento Dificultad"), # Ver un Movimiento

    # Score
    path("crearScore/", crearScore, name="Crear Score"), # Crear Score
    path("listaScore/", verScore, name = "Ver Scores"), # Todos los Scores
    path("listaScoreFiltro/", verScore, name = "Ver Scores Filtrados"), # Todos los Scores filtrados
    

    path("borrar_wod/<wod_nombre>", borrarWod, name="Borrar Wod"),
    path("editarWods/<wod_nombre>", editarWod, name="Editar Wod"), # Crear Wod


    path("borrar_movimiento/<movimiento_nombre>", borrarMovimiento, name="Borrar Movimiento"),
    path("editarmovimiento/<movimiento_nombre>", editarMovimiento, name="Editar Movimiento"), # Crear Wod 
    path("cargarAdaptacion/<movimiento_nombre>", cargarAdaptacionMovimiento, name="Cargar Adaptacion Movimiento"), # Crear Wod 

    
    path("cargarScoreDelDia/<wod_nombre>", cargarScoreDelDia, name="Score del Dia"), # Crear Wod 
    path("uploadAvatar/", upload_avatar, name="Cambiar Avatar"), # Crear Wod 
    path("dejarComentario/<wod_nombre>", dejar_comentario, name="Dejar Comentario"), # Crear Wod 

    
    path("listCompetencias/", verCompetencias, name = "Ver Competencias"), # Todos los Movimientos
    path("crearCompetencia/", crearCompetencias, name="Crear Competencias"), # Crear Movimiento 
    path("verCompetencia/<competencia_nombre>", verCompetencia, name="Ver Competencia"), # Crear Movimiento 
    
    path("about/", about, name="About"), # Ver un Wod 
    path("registro2/", registro2, name="registro2"), # Ver un Wod 
    
  


]
