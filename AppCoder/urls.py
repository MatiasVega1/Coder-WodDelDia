from django.urls import path
from AppCoder.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [ 
    path("", inicio), 
    path("main/", inicio, name = "Start"), 

    # Autenticación
    path("registro/", registro, name="Sign Up"),
    path("registro2/", registro2, name="registro2"), # Ver un Wod 
    path("login/", iniciarSesion, name="Log In"),
    path("logout/", LogoutView.as_view(template_name = "AppCoder/Usuario/logout.html"), name="Log Out"),

    # Atletas
    path("listaAtletas/", verAtletas, name = "Ver Atletas"), # Todos los Atletas 
    path("atleta/borrar/<int:pk>", AtletaBorrar.as_view(), name = "Borrar Atleta"),
    path("ateta/editar/<int:pk>", AtletaEditar.as_view(), name = "Editar Atleta"),

    # Wod
    path("listaWods/", verWods, name = "Ver Wods"), # Todos los Wod
    path("crearWods/", crearWods, name="Crear Wod"), # Crear Wod 
    path("verWod/<wod_nombre>", verWod, name="Filtrar Wod"), # Ver un Wod 
    path("filtrarWod/", filtrarWod, name="Filtrar Wod Tipo"), # Ver un Wod  
    path("borrar_wod/<wod_nombre>", borrarWod, name="Borrar Wod"),
    path("editarWods/<wod_nombre>", editarWod, name="Editar Wod"), # Crear Wod
    path("dejarComentario/<wod_nombre>", dejar_comentario, name="Dejar Comentario"), # Crear Wod 
 
    # Movimientos
    path("listaMovimientos/", verMovimientos, name = "Ver Movimientos"), # Todos los Movimientos
    path("crearMovimientos/", crearMovimientos, name="Crear Movimientos"), # Crear Movimiento 
    path("verMovimiento/<movimiento_nombre>", verMovimiento, name="Filtrar Movimiento"), # Ver un Movimiento
    path("filtrarMovimiento/", filtrarMovimiento, name="Filtrar Movimiento Dificultad"), # Ver un Movimiento
    path("borrar_movimiento/<int:pk>", borrarMovimiento.as_view(), name="Borrar Movimiento"),
    path("editarmovimiento/<movimiento_nombre>", editarMovimiento, name="Editar Movimiento"), # Crear Wod 
    path("cargarAdaptacion/<movimiento_nombre>", cargarAdaptacionMovimiento, name="Cargar Adaptacion Movimiento"), # Crear Wod 

    # Score 
    path("listaScore/", verScore, name = "Ver Scores"), # Todos los Scores 
    path("cargarScoreDelDia/<wod_nombre>", cargarScoreDelDia, name="Score del Dia"), # Crear Wod  

    # Competencias
    path("listCompetencias/", verCompetencias, name = "Ver Competencias"), # Todos los Movimientos
    path("crearCompetencia/", crearCompetencias, name="Crear Competencias"), # Crear Movimiento 
    path("verCompetencia/<competencia_nombre>", verCompetencia, name="Ver Competencia"), # Crear Movimiento 

    # Usuario
    path("uploadAvatar/", upload_avatar, name="Cambiar Avatar"), # Crear Wod 
    path("about/", about, name="About"), # Ver un Wod 
]
