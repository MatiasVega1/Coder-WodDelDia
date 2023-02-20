from django.shortcuts import render, redirect
from django.http import HttpResponse
from AppCoder.models import *
from AppCoder.forms import * 

from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.forms import formset_factory
from django.shortcuts import render  

import random
from datetime import datetime, timedelta


# Paginas de Inicio

def inicio(request):
    return render(request, "AppCoder/inicio.html")

def about(request):
    return render(request, "AppCoder/about.html")


def registro(request):
    print("llegue")
    
    if request.method == 'POST':
        miFormulario = RegistroFormulario(request.POST)
        miFormularioAtleta = AtletaFormulario(request.POST)
        
        print("post")

        if miFormulario.is_valid():
            print("guardand")
            miFormulario.save() 


            # Después de crear el usuario, autenticamos el usuario y lo logueamos
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
        
            return redirect('registro2')

    else:
        miFormulario = RegistroFormulario()
        miFormularioAtleta = AtletaFormulario()
    
    return render(request, "AppCoder/registro.html", {"miFormulario": miFormulario, "miFormularioAtleta": miFormularioAtleta})



def registro2(request):
    print("llegue registro2")
    
    nacionalidades = NACIONALIDAD
    box = Box.objects.all()
  
    
    if request.method == 'POST': 
        miFormularioAtleta = AtletaFormulario(request.POST)
        user = User.objects.get(pk=request.user.pk)
        
        print("entro atleta registro2")
        print(miFormularioAtleta)

        if  miFormularioAtleta.is_valid():
            
            print("Llegue aca1")
            infoDic = miFormularioAtleta.cleaned_data # La info formulario pasa a diccionario
            print("Llegue aca")

            atl1 = Atleta(  usuario = user,
                            nombre = user.first_name, 
                            apellido = user.last_name, 
                            edad = infoDic["edad"],
                            email = user.email,
                            box = infoDic["box"],
                            nacionalidad = infoDic["nacionalidad"])
            atl1.save() 

            print(atl1)
            
            listaAtletas = Atleta.objects.all() 
            
            return render(request, "AppCoder/Atleta/listaAtletas.html", {"listaAtletas": listaAtletas, "nacionalidades": nacionalidades})

    else: 
        miFormularioAtleta = AtletaFormulario()
    
    return render(request, "AppCoder/registro2.html", { "miFormularioAtleta": miFormularioAtleta, "nacionalidades": nacionalidades, "boxes": box})

def iniciarSesion(request): 
    
    if request.method == 'POST':
        miFormulario = AuthenticationForm(request, data = request.POST)
         

        if miFormulario.is_valid(): 
            usuario = miFormulario.cleaned_data.get("username")
            contra = miFormulario.cleaned_data.get("password")

            miUsuario = authenticate(username = usuario, password = contra) # autentica datos
            print(usuario)
            if miUsuario:
                login(request, miUsuario)
                mensaje = f"Bienvenido {miUsuario}"
                return render(request, "AppCoder/inicio.html", {"mensaje":mensaje})
        else:
            mensaje = f"Error. Ingresaste mal los datos"
            return render(request, "AppCoder/inicio.html",  {"mensaje":mensaje})    

    else:
        miFormulario = AuthenticationForm()
    
    return render(request, "AppCoder/login.html", {"miFormulario": miFormulario})

# ABM de Atletas
def verAtletas(request): # Listado principal, ve todos los atletas
    listaAtletas = Atleta.objects.all() 

    for x in listaAtletas:
        print (x)

    # Obtener la longitud del listado original de objetos Atleta
    n = len(listaAtletas)

    # Usar el método "slice" para obtener los últimos 3 objetos Atleta
    ultimos_tres_atletas = listaAtletas[n-3:]

    # Crear un nuevo listado y agregar los objetos Atleta obtenidos
    nuevos_atletas = []
    for atleta in ultimos_tres_atletas:
        nuevos_atletas.append(atleta)

    for atleta in listaAtletas:
        # Para cada objeto Atleta, se obtiene el objeto Avatar correspondiente utilizando la relación inversa generada automáticamente por Django
        print(atleta.usuario)
        userAtleta = User.objects.get(username= atleta.usuario)
        print(userAtleta)
        avatar = AvatarImagen.objects.filter(usuario = userAtleta) 
 
        for x in avatar:
            ava = x 


        print(ava)
        atleta.avatar = ava # Se agrega el objeto Avatar como un atributo del objeto Atleta para poder acceder a él desde la plantilla
        print(atleta.avatar.imagen.url)
    print("asda")
    for x in listaAtletas:
        print(x.avatar.imagen.url)

    return render(request, "AppCoder/Atleta/listaAtletas.html", {"listaAtletas": listaAtletas, "ultimosAtletas": nuevos_atletas})

def crearAtletas(request):
    nacionalidades = NACIONALIDAD
    box = Box.objects.all()
 
    if request.method == 'POST':
        
        print("aaaaaaaa Llegue aca")
        miFormulario = AtletaFormulario(request.POST)
        user = User.objects.get(pk=request.user.pk)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario
            print("Llegue aca")

            atl1 = Atleta(  usuario = user,
                            nombre = infoDic["nombre"], 
                            apellido = infoDic["apellido"], 
                            edad = infoDic["edad"],
                            email = infoDic["email"],
                            box = infoDic["box"],
                            nacionalidad = infoDic["nacionalidad"])
            atl1.save() 

            
            listaAtletas = Atleta.objects.all() 


            return render(request, "AppCoder/Atleta/listaAtletas.html", {"listaAtletas": listaAtletas, "nacionalidades": nacionalidades})
    else:
        miFormulario = AtletaFormulario()

    return render(request, "AppCoder/Atleta/crearAtletas.html", {"formulario1":miFormulario, "nacionalidades": nacionalidades, "boxes": box})



def verAtleta(request):
    if request.GET["apellido"]:

        apellido = request.GET['apellido'] 
        
        atleta1 = Atleta.objects.filter(apellido__icontains= apellido)
        return render(request, "AppCoder/Atleta.verAtleta.html", { "atleta": atleta1, 
                                                            "apellido": apellido})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta)


def filtrarWod(request):
    if request.GET["tipo"]:

        apellido = request.GET['tipo'] 
        
        atleta1 = Wod.objects.filter(tipo__icontains= apellido)
        return render(request, "AppCoder/Wod/verWod.html", {"wods": atleta1})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta, {"wods":atleta1})

def filtrarMovimiento(request):
    if request.GET["dificultad"]:

        apellido = request.GET['dificultad'] 
        
        atleta1 = Movimiento.objects.filter(dificultad__icontains= apellido)
        return render(request, "AppCoder/Movimiento/verMovimiento.html", {"movimientos":atleta1})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta, {"movimientos":atleta1})


# ABM de Wods
def verWods(request): # Listado principal, ve todos los wods
    listaWods = Wod.objects.all() 
    return render(request, "AppCoder/Wod/listaWods.html", {"listaWods": listaWods})

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


''' 
def verWod(request):
    if request.GET["tipo"]:

        tipo = request.GET['tipo'] 
        
        wod1 = Wod.objects.filter(tipo__icontains= tipo)
        return render(request, "AppCoder/detalleWod.html", { "wod": wod1, 
                                                            "tipo": tipo})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta) 
'''


# ABM de Wods
def verWod(request, wod_nombre): # Listado principal, ve todos los wods
    wod1 = Wod.objects.get(nombre = wod_nombre)
    print(wod1)
    comentarios = Comentario.objects.filter(wod = wod1) 

    
    scores = Score.objects.filter(wod = wod1)

    atletas_scores = {}
    
    for score in scores:
        atleta = score.atleta # revisar
        if atleta in atletas_scores:
            atletas_scores[atleta] += score.score
        else:
            atletas_scores[atleta] = score.score
    
    ranking = sorted(atletas_scores.items(), key=lambda x: x[1], reverse=True)


    return render(request, "AppCoder/Wod/detalleWod.html", {"wod": wod1, "comentarios": comentarios, "listaScores": ranking})

# ABM de Movimientos
def verMovimientos(request): # Listado principal, ve todos los movimientos
    listaMovimientos = Movimiento.objects.all() 
    return render(request, "AppCoder/Movimiento/listaMovimientos.html", {"listaMovimientos": listaMovimientos})

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
            
            print("ASD", infoDic["dificultad"])

            listaMovimientos = Movimiento.objects.all() 
            return render(request, "AppCoder/Movimiento/listaMovimientos.html", {"listaMovimientos": listaMovimientos})
    else:
        miFormulario = MovimientoFormulario()

    return render(request, "AppCoder/Movimiento/crearMovimientos.html", {"formulario1":miFormulario})

def verMovimiento(request, movimiento_nombre): # Listado principal, ve todos los atletas
    
    mov1 = Movimiento.objects.get(nombre = movimiento_nombre)
 
    ada1 = Adaptacion.objects.filter(movimiento = mov1)

 
    #comentarios = Comentario.objects.filter(wod = wod1) 

    
    #scores = Score.objects.filter(wod = wod1) 

    return render(request, "AppCoder/Movimiento/detalleMovimiento.html", {"movimiento": mov1, "listaAdaptacion": ada1 })



# ABM de Movimientos
def verScore(request): # Listado principal, ve todos los scores
    # Acá obtengo todos los scores, pero quiero ordenarlos de mayor a menor para mostrar los mejores
    listaScores = Score.objects.all().order_by("-score") 

    wodDelDia = Wod.objects.all()
  
    # obtener el objeto aleatorio de la lista
    objeto_aleatorio = random.choice(wodDelDia)
    scores = Score.objects.all()

    atletas_scores = {}
    
    for score in scores:
        atleta = score.atleta # revisar
        if atleta in atletas_scores:
            atletas_scores[atleta] += score.score
        else:
            atletas_scores[atleta] = score.score
    
    ranking = sorted(atletas_scores.items(), key=lambda x: x[1], reverse=True)

     

    return render(request, "AppCoder/Score/listaScores.html", {"listaScores": ranking ,  "wodDelDia": objeto_aleatorio })

@login_required
def crearScore(request):
    listaWods = Wod.objects.all()

    print(request)
    
    if request.method == 'POST':
        
        miFormulario = ScoreFormulario(request.POST)
        
        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario

            print(infoDic)
           # wod1 = Wod() 

            sco1 = Score(   fecha = infoDic["fecha"],  
                            score = infoDic["score"],  
                            wod = infoDic["wod"],  
                            atleta = infoDic["atleta"], )

   
            sco1.save() 
             
            return render(request, "AppCoder/Score/listaScores.html")
    else:
        miFormulario = ScoreFormulario()

    return render(request, "AppCoder/Score/crearScore.html", {"formulario1":miFormulario, "wods": listaWods})


def borrarWod(request, wod_nombre):
    wodBorrar = Wod.objects.get(nombre = wod_nombre)
    wodBorrar.delete()

    return render(request, "AppCoder/inicio.html")

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

            
            listaWods = Wod.objects.all() 

            return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = WodFormulario(initial={  "nombre": wodEditar.nombre, 
                                                "tipo": wodEditar.tipo, 
                                                "duracion": wodEditar.duracion})

    return render(request, "AppCoder/Wod/editarWods.html", {"formulario1":miFormulario}) 


@login_required
def cargarScoreDelDia(request, wod_nombre):
    miFormulario = ScoreFormulario(request.POST)

    wodCargarScoreObjeto = Wod.objects.get(nombre = wod_nombre)
    print(wodCargarScoreObjeto)
    wodCargarScore = Wod.objects.filter(nombre = wod_nombre) 
    print("asddd")
    if miFormulario.is_valid():
        infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario  
        print("aaaaaaaaaasddd")

        sco1 = Score(   fecha = infoDic["fecha"],  
                            score = infoDic["score"],  
                            wod = wodCargarScoreObjeto,  
                            atleta = infoDic["atleta"], )

         
        print("sxxxxxxxxxxasddd")
        sco1.save() 
        
        print("aaaaaaaaaa")
        return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = ScoreFormulario()

    return render(request, "AppCoder/Score/crearScore.html", {"formulario1":miFormulario, "wodDelDia":True, "wods": wodCargarScore})
    




def borrarMovimiento(request, movimiento_nombre):
    movBorrar = Movimiento.objects.get(nombre = movimiento_nombre)
    movBorrar.delete()

    return render(request, "AppCoder/Score/listaScores.html")

def editarMovimiento(request, movimiento_nombre):

    movEditar = Movimiento.objects.get(nombre = movimiento_nombre)

    print(movEditar)

    if request.method == 'POST':
        
        miFormulario = MovimientoFormulario(request.POST, request.FILES)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario

            movEditar.nombre = infoDic["nombre"]
            movEditar.descripcion = infoDic["descripcion"]
            movEditar.dificultad = infoDic["dificultad"]
            movEditar.explicacion = infoDic["explicacion"]
            movEditar.imagen = infoDic["imagen"]

            print(infoDic["imagen"])
            print(infoDic)
             
            movEditar.save() 

            
            listaWods = Movimiento.objects.all() 

            return render(request, "AppCoder/inicio.html")
    else:
        miFormulario = MovimientoFormulario(initial={  "nombre": movEditar.nombre, 
                                                "descripcion": movEditar.descripcion, 
                                                "dificultad": movEditar.dificultad,
                                                "imagen": movEditar.imagen,
                                                "explicacion": movEditar.explicacion})

    return render(request, "AppCoder/Movimiento/editarMovimiento.html", {"formulario1":miFormulario}) 


class AtletaLista(ListView):
    model = Atleta
    template_name = "AppCoder/Atleta/atleta_list.html"
    variable = "hola"

class AtletaCrear(LoginRequiredMixin, CreateView):
    model = Atleta
    fields = ["nombre", "apellido", "edad", "email"]

class AtletaBorrar(DeleteView):
    model = Atleta
    success_url = "/AppCoder/listaAtletasLista"
    template_name = "AppCoder/Atleta/atleta_borrar.html"

class AtletaEditar(UpdateView):
    model = Atleta
    fields = ["nombre", "apellido", "edad", "email"]
    success_url = "/AppCoder/Atleta/listaAtletasLista"
   #lo  template_name = "AppCoder/atleta_list.html"  


def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarImagenFormulario(request.POST, request.FILES)
        if form.is_valid():
            userImg = User.objects.get(pk=request.user.pk)
            print(userImg)
            #avatarImg = AvatarImagen()
            #avatarImg = form.cleaned_data['imagen']
            infoDic = form.cleaned_data
            print(infoDic)

            ava1 = AvatarImagen(   usuario = userImg,  
                                imagen = infoDic["imagen"] )


            ava1.save()
            return render(request, "AppCoder/inicio.html")
    else:
        form = AvatarImagenFormulario()
    return render(request, 'AppCoder/cambiarAvatar.html', {'form': form})


@login_required
def dejar_comentario(request, wod_nombre):
    wodCargarScoreObjeto = Wod.objects.get(nombre = wod_nombre)
    print(wodCargarScoreObjeto)
    wodCargarScore = Wod.objects.filter(nombre = wod_nombre) 
    
    if request.method == 'POST':
        
        form = ComentarioFormulario(request.POST, request.FILES)

        if form.is_valid():
            userComentario = User.objects.get(pk=request.user.pk)
            
            #avatarImg = AvatarImagen()
            #avatarImg = form.cleaned_data['imagen']
            infoDic = form.cleaned_data
            print(infoDic)

            comentario1 = Comentario(   usuario = userComentario,  
                                        wod = infoDic["wod"],
                                        #fecha = datetime.today(),
                                        comentario = infoDic["comentario"]
                                        #titulo = infoDic["titulo"] 
                                        )


            comentario1.save()
            return render(request, "AppCoder/inicio.html")
    else:
        form = ComentarioFormulario()
    return render(request, 'AppCoder/Wod/dejarComentario.html', {'form': form , "wods": wodCargarScore})



    
@login_required
def cargarAdaptacionMovimiento(request, movimiento_nombre): 

    print(movimiento_nombre)

    movimientoObjeto = Movimiento.objects.get(nombre = movimiento_nombre)
     
    wodCargarScore = Movimiento.objects.filter(nombre = movimiento_nombre) 
    
    if request.method == 'POST':
        
        form = AdaptacionFormulario(request.POST, request.FILES)

        if form.is_valid():
            userComentario = User.objects.get(pk=request.user.pk)
            
            #avatarImg = AvatarImagen()
            #avatarImg = form.cleaned_data['imagen']
            infoDic = form.cleaned_data
            print(infoDic)

            adaptacion1 = Adaptacion(   movimiento = movimientoObjeto,
                                        nombre = infoDic["nombre"],    
                                        descripcion = infoDic["descripcion"],
                                        explicacion = infoDic["explicacion"] )


            adaptacion1.save()
            return render(request, "AppCoder/inicio.html")
    else:
        form = AdaptacionFormulario()
    return render(request, 'AppCoder/Wod/dejarComentario.html', {'form': form , "wods": wodCargarScore})



# ABM de Movimientos
def verCompetencias(request): # Listado principal, ve todos los movimientos
    listaMovimientos = Competencia.objects.all() 
    return render(request, "AppCoder/Competencia/listaCompetencias.html", {"listaMovimientos": listaMovimientos})

def crearCompetencias(request):
    if request.method == 'POST':
        
        miFormulario = CompetenciaFormulario(request.POST, request.FILES)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario
            print(infoDic)

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


def verCompetencia(request, competencia_nombre): # Listado principal, ve todos los wods

    competencia1 = Competencia.objects.get(nombre = competencia_nombre)
    atletas = Atleta.objects.all()

    
    todosScoreCompe = ScoreCompetencia.objects.all()
    todosScoreCompe.delete()

    print(competencia1.wod1)

    for x in atletas:
        avatar = AvatarImagen.objects.get(usuario = x.usuario)
        avatarUrl = avatar.imagen
        print("arranca")
        scoreWod1 = x.getScoreWod(competencia1.wod1)
        scoreWod2 = x.getScoreWod(competencia1.wod2)
        scoreWod3 = x.getScoreWod(competencia1.wod3)
        print(avatarUrl)
        if (scoreWod1 > 0 or scoreWod2 > 0 or scoreWod3 > 0 ):
            print("llegue")
            comp1 = ScoreCompetencia(   atleta = x,
                                            imagen = avatarUrl, 
                                            wod1 = scoreWod1,
                                            wod2 = scoreWod2,
                                            wod3 = scoreWod3,
                                            total = scoreWod1 + scoreWod2 + scoreWod3)
            
            comp1.save() 
            print(comp1)     
        
            
    scores = ScoreCompetencia.objects.all().order_by('-total')
 

    return render(request, "AppCoder/Competencia/detalleCompetencia.html", {"competencia": competencia1, "listaScores": scores})