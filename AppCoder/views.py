from django.shortcuts import render, redirect
from django.http import HttpResponse

from AppCoder.models import *
from AppCoder.forms import * 

from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required 

import random
from django.conf import settings
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required


###########################################################################
# PAGINAS DE USUARIO
###########################################################################
# Acá se encuentran todas las paginas que se refieren al ABM de usuarios: 
# Inicio y cierre de sesión
# Página sobre mi
# Registro: Paso 1 y 2
# Actualizar Avatar
###########################################################################


# Página de inicio para ver siempre que se ingresa a la web
def inicio(request):
    return render(request, "AppCoder/inicio.html")

# Vista de página About
def about(request):
    return render(request, "AppCoder/about.html")

# Registro Paso 1: Completar datos del usuario
def registro(request):     
    if request.method == 'POST':
        miFormulario = RegistroFormulario(request.POST)
        
        if miFormulario.is_valid(): 
            miFormulario.save() 

            # Después de crear el usuario, autenticamos el usuario y lo logueamos
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)

            # Una vez que se logueó el usuario, redirigimos al paso 2
            return redirect('registro2')

    else:
        miFormulario = RegistroFormulario() 
    
    return render(request, "AppCoder/Usuario/registro.html", {"miFormulario": miFormulario})

# Registro Paso 2: Completar datos de atleta
def registro2(request): 
    # Voy a necesitar completar dos listas de valores: Nacionalidad y Box
    # Nacionalidad lo obtengo de una de mis constantes estáticas
    nacionalidades = NACIONALIDAD
    # Box lo obtengo desde el listado de todos los box que tengo cargados
    # Por ahora solo tres, únicamente para el ejemplo
    box = Box.objects.all()
    
    if request.method == 'POST': 
        miFormularioAtleta = AtletaFormulario(request.POST)
        # Como voy a necesitar relacionar 1 a 1 mi atleta con mi usuario
        # Obtengo los datos del usuario para luego guardarlo
        user = User.objects.get(pk=request.user.pk)

        if  miFormularioAtleta.is_valid():
             
            infoDic = miFormularioAtleta.cleaned_data  

            atl1 = Atleta(  usuario = user, # Lo relaciono al usuario que se dió de alta
                            nombre = user.first_name, # No es necesario pero lo hago igual
                            apellido = user.last_name, # No es necesario pero lo hago igual
                            edad = infoDic["edad"],
                            email = user.email, 
                            box = infoDic["box"],
                            nacionalidad = infoDic["nacionalidad"])
            atl1.save() 
 
            listaAtletas = Atleta.objects.all() 
            
            return render(request, "AppCoder/inicio.html", {"listaAtletas": listaAtletas})

    else: 
        miFormularioAtleta = AtletaFormulario()
    
    return render(request, "AppCoder/Usuario/registro2.html", { "miFormularioAtleta": miFormularioAtleta, "nacionalidades": nacionalidades, "boxes": box})

# Página de inicio de sesión
def iniciarSesion(request): 
    
    if request.method == 'POST':
        miFormulario = AuthenticationForm(request, data = request.POST)

        if miFormulario.is_valid(): 
            usuario = miFormulario.cleaned_data.get("username")
            contra = miFormulario.cleaned_data.get("password")

            miUsuario = authenticate(username = usuario, password = contra) # autentica datos 
            if miUsuario:
                login(request, miUsuario)
                mensaje = f"Bienvenido {miUsuario}"
                # Envio los datos por mensaje para que se imprima
                return render(request, "AppCoder/inicio.html", {"mensaje":mensaje})
        else:
            mensaje = f"Error. Ingresaste mal los datos"
            # Envio los datos por mensaje para que se imprima
            return render(request, "AppCoder/inicio.html",  {"mensaje":mensaje})    

    else:
        miFormulario = AuthenticationForm()
    
    return render(request, "AppCoder/Usuario/login.html", {"miFormulario": miFormulario})

# Página para cargar un nuevo Avatar
@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarImagenFormulario(request.POST, request.FILES)
        if form.is_valid():
            userImg = User.objects.get(pk=request.user.pk) 
            infoDic = form.cleaned_data 

            # Mi formulario solo permite subir una imagen, el resto lo obtengo de mi usuario logueado
            ava1 = AvatarImagen(   usuario = userImg,  
                                imagen = infoDic["imagen"] )

            ava1.save()
            return render(request, "AppCoder/inicio.html")
    else:
        form = AvatarImagenFormulario()
    return render(request, 'AppCoder/Usuario/cambiarAvatar.html', {'form': form})

###########################################################################
# PAGINAS DE ABM de WOD
###########################################################################
# Acá se encuentran todas las paginas que se refieren al ABM de Wod
# Un wod es el entrenamiento que se realizará por el atleta 
# Se permitirá a cualquier usuario ver y filtrar el listado de wods y ver el detalle
# Sólo a usuarios logueados se les permitirá cargar un score y dejar comentario
# Sólo a usuarios staff se les permitirá eliminar, editar y crear wods 
###########################################################################

# Listado principal para ver todos los wods
def verWods(request):  
    listaWods = Wod.objects.all() # Obtengo todos los wods
    return render(request, "AppCoder/Wod/listaWods.html", {"listaWods": listaWods})

# Quiero crear un nuevo wod
# Solo pueden crearlo aquellos que son staff
@staff_member_required
def crearWods(request):
    if request.method == 'POST':
        
        miFormulario = WodFormulario(request.POST)
         
        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario 

            wod1 = Wod(  nombre = infoDic["nombre"], 
                            tipo = infoDic["tipo"], 
                            duracion = infoDic["duracion"],
                            rondas = infoDic["rondas"], 
                            cantidad1 = infoDic["cantidad1"],
                            movimiento1 = infoDic["movimiento1"],
                            cantidad2 = infoDic["cantidad2"],
                            movimiento2 = infoDic["movimiento2"],
                            cantidad3 = infoDic["cantidad3"],
                            movimiento3 = infoDic["movimiento3"],
                            cantidad4 = infoDic["cantidad4"],
                            movimiento4 = infoDic["movimiento4"],
                            cantidad5 = infoDic["cantidad5"],
                            movimiento5 = infoDic["movimiento5"],)
            wod1.save() 

            listaWods = Wod.objects.all() 

            return render(request, "AppCoder/Wod/listaWods.html", {"listaWods": listaWods})
    else:
        miFormulario = WodFormulario()

    return render(request, "AppCoder/Wod/crearWods.html", {"formulario1":miFormulario}) 

# En el listado de wods se permite buscar por tipo
# Este filtro por tipo trae un listado identico al otro pero en otra pagina
def filtrarWod(request):
    if request.GET["tipo"]:

        tipo = request.GET['tipo']  # Obtengo el tipo seleccionado 
        wodsFiltrados = Wod.objects.filter(tipo__icontains= tipo) # Filtro por tipo

        return render(request, "AppCoder/Wod/verWod.html", {"wods": wodsFiltrados})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta, {"wods":wodsFiltrados})

# Eliminar wod
@staff_member_required
def borrarWod(request, wod_nombre):
    wodBorrar = Wod.objects.get(nombre = wod_nombre)
    wodBorrar.delete()

    return render(request, "AppCoder/inicio.html")

# Editar wod
@staff_member_required
def editarWod(request, wod_nombre): 
    wodEditar = Wod.objects.get(nombre = wod_nombre)

    if request.method == 'POST':        
        miFormulario = WodFormulario(request.POST)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario

            wodEditar.nombre = infoDic["nombre"]
            wodEditar.tipo = infoDic["tipo"]
            wodEditar.duracion = infoDic["duracion"]

            wodEditar.save()

            return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = WodFormulario(initial={  "nombre": wodEditar.nombre, 
                                                "tipo": wodEditar.tipo, 
                                                "duracion": wodEditar.duracion})

    return render(request, "AppCoder/Wod/editarWods.html", {"formulario1":miFormulario}) 

# Ver wod en detalle
def verWod(request, wod_nombre):  
    # Necesito traer los datos del wod
    wod1 = Wod.objects.get(nombre = wod_nombre) 
    # Quiero traerme todos los comentarios del wod en cuestión
    comentarios = Comentario.objects.filter(wod = wod1)  
    # Llamo a la función calcular Scores con el wod correspondiente
    ranking = calcularScores(wod1)

    return render(request, "AppCoder/Wod/detalleWod.html", {"wod": wod1, "comentarios": comentarios, "listaScores": ranking})

# Vista para dejar comentario
@login_required
def dejar_comentario(request, wod_nombre):
    wodCargarScoreObjeto = Wod.objects.get(nombre = wod_nombre) 
    wodCargarScore = Wod.objects.filter(nombre = wod_nombre) 
    
    if request.method == 'POST':        
        form = ComentarioFormulario(request.POST, request.FILES)

        if form.is_valid():
            userComentario = User.objects.get(pk=request.user.pk)
            infoDic = form.cleaned_data 

            comentario1 = Comentario(   usuario = userComentario,  
                                        wod = wodCargarScoreObjeto,
                                        fecha = datetime.today(),
                                        comentario = infoDic["comentario"],
                                        titulo = infoDic["titulo"])
            comentario1.save()
            return render(request, "AppCoder/inicio.html")
    else:
        form = ComentarioFormulario()
    return render(request, 'AppCoder/Wod/dejarComentario.html', {'form': form , "wods": wodCargarScore})

###########################################################################
# PAGINAS DE ABM de MOVIMIENTOS
###########################################################################
# Acá se encuentran todas las paginas que se refieren al ABM de Movimientos
# Un wod está conformado por distintos movimientos
# Se permitirá a cualquier usuario ver y filtrar el listado de movimientos y ver el detalle 
# Sólo a usuarios staff se les permitirá eliminar, editar y crear movimientos 
###########################################################################

# Listado principal, ve todos los movimientos
def verMovimientos(request): 
    listaMovimientos = Movimiento.objects.all() 
    return render(request, "AppCoder/Movimiento/listaMovimientos.html", {"listaMovimientos": listaMovimientos})

# Permite crear movimiento
@staff_member_required
def crearMovimientos(request):
    if request.method == 'POST':
        
        miFormulario = MovimientoFormulario(request.POST, request.FILES)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario

            mov1 = Movimiento(  nombre = infoDic["nombre"], 
                            descripcion = infoDic["descripcion"], 
                            dificultad = infoDic["dificultad"],
                            explicacion = infoDic["explicacion"],
                            imagen = infoDic["imagen"])
            mov1.save() 

            listaMovimientos = Movimiento.objects.all() 
            return render(request, "AppCoder/Movimiento/listaMovimientos.html", {"listaMovimientos": listaMovimientos})
    else:
        miFormulario = MovimientoFormulario()

    return render(request, "AppCoder/Movimiento/crearMovimientos.html", {"formulario1":miFormulario})

# Ver el movimiento
def verMovimiento(request, movimiento_nombre):  
    # Necesito obtener los datos del movimiento
    mov1 = Movimiento.objects.get(nombre = movimiento_nombre)
    # Cuando ingreso al detalle de un movimiento, necesito cargar todas las adaptaciones cargadas
    ada1 = Adaptacion.objects.filter(movimiento = mov1)

    return render(request, "AppCoder/Movimiento/detalleMovimiento.html", {"movimiento": mov1, "listaAdaptacion": ada1 })

# Filtrar movimiento se realiza por dificultad
def filtrarMovimiento(request):
    if request.GET["dificultad"]:

        dificultad = request.GET['dificultad'] 
        # Obtengo todos los movimientos filtrando por dificultad
        movFiltrados = Movimiento.objects.filter(dificultad__icontains= dificultad)

        return render(request, "AppCoder/Movimiento/verMovimiento.html", {"movimientos":movFiltrados})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta, {"movimientos":movFiltrados})

# Editar movimientos
@staff_member_required
def editarMovimiento(request, movimiento_nombre):
    movEditar = Movimiento.objects.get(nombre = movimiento_nombre) 

    if request.method == 'POST':        
        miFormulario = MovimientoFormulario(request.POST, request.FILES)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario

            movEditar.nombre = infoDic["nombre"]
            movEditar.descripcion = infoDic["descripcion"]
            movEditar.dificultad = infoDic["dificultad"]
            movEditar.explicacion = infoDic["explicacion"]
            movEditar.imagen = infoDic["imagen"]
 
            movEditar.save()  

            return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = MovimientoFormulario(initial={  "nombre": movEditar.nombre, 
                                                "descripcion": movEditar.descripcion, 
                                                "dificultad": movEditar.dificultad,
                                                "imagen": movEditar.imagen,
                                                "explicacion": movEditar.explicacion})

    return render(request, "AppCoder/Movimiento/editarMovimiento.html", {"formulario1":miFormulario}) 

# A cualquier movimiento se le puede cargar una adaptación
# Una adaptación es el mismo movimiento pero realizado más facil
@login_required
def cargarAdaptacionMovimiento(request, movimiento_nombre): 
    movimientoObjeto = Movimiento.objects.get(nombre = movimiento_nombre)     
    wodCargarScore = Movimiento.objects.filter(nombre = movimiento_nombre) 
    
    if request.method == 'POST':        
        form = AdaptacionFormulario(request.POST, request.FILES)

        if form.is_valid(): 
            infoDic = form.cleaned_data 

            adaptacion1 = Adaptacion(   movimiento = movimientoObjeto,
                                        nombre = infoDic["nombre"],    
                                        descripcion = infoDic["descripcion"],
                                        explicacion = infoDic["explicacion"] ) 
            adaptacion1.save()
            return render(request, "AppCoder/inicio.html")
    else:
        form = AdaptacionFormulario()
    return render(request, 'AppCoder/Wod/dejarComentario.html', {'form': form , "wods": wodCargarScore})

# Permite eliminar un movimiento
class borrarMovimiento(DeleteView):
    model = Movimiento
    
    success_url = "/AppCoder/listaMovimientos"
    template_name = "AppCoder/Movimiento/movimiento_confirm_delete.html"


###########################################################################
# PAGINAS DE ABM de SCORES
###########################################################################
# Acá se encuentran todas las paginas que se refieren al ABM de Scores
# Un atleta recibe puntos al realizar un wod
# Se permitirá a cualquier usuario ver todos los scores
# También puede ver el score de un wod en particular
# Sólo a usuarios logueados se les permitirá crear scores 
###########################################################################

# Función para calcular el score de un wod
# Lo armé en una función aparte porque asi podía reutilizar código
def calcularScores(wod1): # Recibe como parametro el wod 
    if wod1: # Si recibe un wod filtro por él
        # Obtengo el listado de scores para el wod en cuestión
        scores = Score.objects.filter(wod = wod1) 
    else: # Si no recibo un wod, es porque se realizará para todos los scores en general
        # Obtengo todos los scores
        scores = Score.objects.all()

    # Defino un diccionario para almacenar el score por cada atleta
    atletas_scores = {}
    
    # Recorro mi listado de scores
    for score in scores: 
        atleta = score.atleta # Obtengo el atleta de mi listado de scores
        if atleta in atletas_scores: # Si ya existe en mi diccionario, lo sumo
            atletas_scores[atleta] += score.score
        else: # Si no existe, lo cargo en un registro nuevo
            atletas_scores[atleta] = score.score
    
    # Ordeno el listado de scores de cada atleta para ordenarlo
    ranking = sorted(atletas_scores.items(), key=lambda x: x[1], reverse=True)
    # Devuelvo el listado ordenado
    return ranking

# Listado de scores en general
def verScore(request): 
    wodDelDia = Wod.objects.all()

    # obtener el wod del día, se muestra siempre en la página principal
    objeto_aleatorio = random.choice(wodDelDia)
    # Obtengo el listado de los mejores atletas
    # Mando un None para indicarle a la función que debo calcular en general
    ranking = calcularScores(None)

    return render(request, "AppCoder/Score/listaScores.html", {"listaScores": ranking ,  "wodDelDia": objeto_aleatorio })

# Tengo que cargar el nuevo score
@login_required
def cargarScoreDelDia(request, wod_nombre): 
    # Recibo el nombre del wod 
    miFormulario = ScoreFormulario(request.POST)

    # Necesito el Objeto
    wodCargarScoreObjeto = Wod.objects.get(nombre = wod_nombre) 
    wodCargarScore = Wod.objects.filter(nombre = wod_nombre) 

    if miFormulario.is_valid():
        infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario   

        sco1 = Score(   fecha = infoDic["fecha"],  
                            score = infoDic["score"],  
                            wod = wodCargarScoreObjeto,  
                            atleta = infoDic["atleta"], )
          
        sco1.save() 
         
        return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = ScoreFormulario()

    return render(request, "AppCoder/Score/crearScore.html", {"formulario1":miFormulario, "wods": wodCargarScore})


###########################################################################
# PAGINAS DE ABM de ATLETAS
###########################################################################
# Acá se encuentran todas las paginas que se refieren al ABM de Atletas
# Un atleta es nuestro usuario final de la aplicación
# Cada atleta está relacionado 1 a 1 con un usuario
# Se permitirá a cualquier usuario ver todos los atletas 
# Cada usuario tendrá la posibilidad de crear, editar y eliminar sus datos de atleta
###########################################################################

# Ver el listado general de atletas
def verAtletas(request): # Listado principal, ve todos los atletas
    listaAtletas = Atleta.objects.all().order_by('-id') 
    # Me quedo con los últimos 3 atletas de mi listado para mostrar 
    nuevos_atletas = listaAtletas[:3][::-1]

    for atleta in listaAtletas:
        # Para cada objeto Atleta, se obtiene el objeto Avatar correspondiente  
        userAtleta = User.objects.get(username= atleta.usuario) 
        atleta.avatar  = AvatarImagen.objects.filter(usuario = userAtleta).last()
           
    return render(request, "AppCoder/Atleta/listaAtletas.html", {"listaAtletas": listaAtletas, "ultimosAtletas": nuevos_atletas, 'avatar_default_image': settings.AVATAR_DEFAULT_IMAGE})

# Permite eliminar los datos de un atleta 
class AtletaBorrar(LoginRequiredMixin, DeleteView):
    model = Atleta
    success_url = "/AppCoder/listaAtletas"
    template_name = "AppCoder/Atleta/atleta_confirm_delete.html"

# Permite editar los datos de un atleta 
class AtletaEditar(LoginRequiredMixin, UpdateView):
    model = Atleta
    fields = ["nombre", "apellido", "edad", "email"]
    success_url = "/AppCoder/listaAtletas"
    template_name = "AppCoder/Atleta/atleta_form.html"  


###########################################################################
# PAGINAS DE ABM de COMPETENCIAS
###########################################################################
# Acá se encuentran todas las paginas que se refieren al ABM de Competencia
# Una competencia está conformada por tres wod
# Cada atleta realiza el wod y recibe un score
# Se ordenarán los atletas por wod
# Cualquier usuario puede ver el listado y detalle de las competencias
# Solo los usuarios de staff pueden crear competencias
###########################################################################

# Listado de todas las competencias
def verCompetencias(request):  
    listaMovimientos = Competencia.objects.all() 
    return render(request, "AppCoder/Competencia/listaCompetencias.html", {"listaMovimientos": listaMovimientos})

# Crear competencias
@staff_member_required
def crearCompetencias(request):
    if request.method == 'POST':        
        miFormulario = CompetenciaFormulario(request.POST, request.FILES)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario 

            comp1 = Competencia(     nombre = infoDic["nombre"], 
                                    imagen = infoDic["imagen"], 
                                    wod1 = infoDic["wod1"],
                                    wod2 = infoDic["wod2"],
                                    wod3 = infoDic["wod3"] )
            comp1.save()             

            listaCompetencias = Competencia.objects.all() 
            return render(request, "AppCoder/Competencia/listaCompetencias.html", {"listaCompetencias": listaCompetencias})
    else:
        miFormulario = CompetenciaFormulario()

    return render(request, "AppCoder/Competencia/crearCompetencias.html", {"formulario1":miFormulario})

# Ver detalle de competencias
def verCompetencia(request, competencia_nombre): # Recibo como parametro el nombre de la competencia
    # Obtengo los datos de la competencia
    competencia1 = Competencia.objects.get(nombre = competencia_nombre)
    # Obtengo mi listado de todos los atletas
    atletas = Atleta.objects.all()
    # También obtengo todos los scores cargados previamente para eliminarlos
    # Esto lo hago porque lo voy a utilizar luego
    # No es la solución más limpia, podría hacerlo mejor con un timestamp
    todosScoreCompe = ScoreCompetencia.objects.all()
    todosScoreCompe.delete() 

    # Recorro mi listado de ateltas para obtener el score de cada uno
    for x in atletas:    
        # Obtengo el score para cada uno de los wod
        # En mi modelo Atleta existe un metodo getScoreWod que recibe un wod y devuelve un numero de score      
        scoreWod1 = x.getScoreWod(competencia1.wod1)
        scoreWod2 = x.getScoreWod(competencia1.wod2)
        scoreWod3 = x.getScoreWod(competencia1.wod3)    

        # Si el atleta está participando es que tiene cargado un score en alguno de los wod que forman la competencia
        if (scoreWod1 > 0 or scoreWod2 > 0 or scoreWod3 > 0 ): 
            # Creo un objeto de score compentencia
            # Este es directamente el score que obtuvo cada atleta en cada wod para una competencia
            comp1 = ScoreCompetencia(       atleta = x,
                                            # Esto lo hago solo para poder referenciarlo en el html
                                            # Utilizo un if para ver si el atleta tiene avatar o no
                                            # Si tiene, lo obtengo de la función getAvatar del modelo Atleta
                                            # Si no tiene, dejo la URL definida en Settings
                                            imagen = x.getAvatar() if x.getAvatar() else settings.AVATAR_DEFAULT_IMAGE, 
                                            wod1 = scoreWod1,
                                            wod2 = scoreWod2,
                                            wod3 = scoreWod3,
                                            # El total es la suma de los 3 wods
                                            total = scoreWod1 + scoreWod2 + scoreWod3)
            
            comp1.save()    
    # Ordeno mi listado por Total
    scores = ScoreCompetencia.objects.all().order_by('-total') 
    return render(request, "AppCoder/Competencia/detalleCompetencia.html", {"competencia": competencia1, "listaScores": scores})