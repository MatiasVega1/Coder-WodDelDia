from django.shortcuts import render, redirect
from django.http import HttpResponse
from AppCoder.models import *
from AppCoder.forms import * 

# Paginas de Inicio
def inicio(request):
    return render(request, "AppCoder/inicio.html")

# ABM de Atletas
def verAtletas(request): # Listado principal, ve todos los atletas
    listaAtletas = Atleta.objects.all() 
    return render(request, "AppCoder/listaAtletas.html", {"listaAtletas": listaAtletas})

def crearAtletas(request):
    if request.method == 'POST':
        
        miFormulario = AtletaFormulario(request.POST)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario

            atl1 = Atleta(  nombre = infoDic["nombre"], 
                            apellido = infoDic["apellido"], 
                            edad = infoDic["edad"],
                            email = infoDic["email"])
            atl1.save() 

            
            listaAtletas = Atleta.objects.all() 

            return render(request, "AppCoder/listaAtletas.html", {"listaAtletas": listaAtletas})
    else:
        miFormulario = AtletaFormulario()

    return render(request, "AppCoder/crearAtletas.html", {"formulario1":miFormulario})

def verAtleta(request):
    if request.GET["apellido"]:

        apellido = request.GET['apellido'] 
        
        atleta1 = Atleta.objects.filter(apellido__icontains= apellido)
        return render(request, "AppCoder/verAtleta.html", { "atleta": atleta1, 
                                                            "apellido": apellido})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta)


# ABM de Wods
def verWods(request): # Listado principal, ve todos los wods
    listaWods = Wod.objects.all() 
    return render(request, "AppCoder/listaWods.html", {"listaWods": listaWods})

def crearWods(request):
    if request.method == 'POST':
        
        miFormulario = WodFormulario(request.POST)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario

            wod1 = Wod(  nombre = infoDic["nombre"], 
                            tipo = infoDic["tipo"], 
                            duracion = infoDic["duracion"], 
                            movimientos = infoDic["movimientos"])
            wod1.save() 

            
            listaWods = Wod.objects.all() 

            return render(request, "AppCoder/listaWods.html", {"listaWods": listaWods})
    else:
        miFormulario = WodFormulario()

    return render(request, "AppCoder/crearWods.html", {"formulario1":miFormulario}) 

def verWod(request):
    if request.GET["tipo"]:

        tipo = request.GET['tipo'] 
        
        wod1 = Wod.objects.filter(tipo__icontains= tipo)
        return render(request, "AppCoder/verWod.html", { "wod": wod1, 
                                                            "tipo": tipo})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta) 

# ABM de Movimientos
def verMovimientos(request): # Listado principal, ve todos los movimientos
    listaMovimientos = Movimiento.objects.all() 
    return render(request, "AppCoder/listaMovimientos.html", {"listaMovimientos": listaMovimientos})

def crearMovimientos(request):
    if request.method == 'POST':
        
        miFormulario = MovimientoFormulario(request.POST)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario

            mov1 = Movimiento(  nombre = infoDic["nombre"], 
                            descripcion = infoDic["descripcion"], 
                            dificultad = infoDic["dificultad"])
            mov1.save() 
            
            print("ASD", infoDic["dificultad"])

            listaMovimientos = Movimiento.objects.all() 
            return render(request, "AppCoder/listaMovimientos.html", {"listaMovimientos": listaMovimientos})
    else:
        miFormulario = MovimientoFormulario()

    return render(request, "AppCoder/crearMovimientos.html", {"formulario1":miFormulario})

def verMovimiento(request): # Listado principal, ve todos los atletas
    if request.GET["dificultad"]:

        dificultad = request.GET['dificultad'] 
        
        mov1 = Movimiento.objects.filter(dificultad__icontains= dificultad)
        return render(request, "AppCoder/verMovimiento.html", { "movimiento": mov1, 
                                                                "dificultad": dificultad})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta)


# ABM de Movimientos
def verScore(request): # Listado principal, ve todos los scores
    listaScores = Score.objects.all() 
    return render(request, "AppCoder/listaScores.html", {"listaScores": listaScores})

def crearScore(request):
    if request.method == 'POST':
        
        miFormulario = ScoreFormulario(request.POST)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario

            wod1 = Wod()

            print(infoDic)

            sco1 = Score(   fecha = infoDic["fecha"],  
                            score = infoDic["score"],  
                            wod = infoDic["wod"],  
                            atleta = infoDic["atleta"], )

   
            sco1.save() 
            
            #listaWods = Wod.objects.all() 
            #listaAtletas = Wod.objects.all() 

            return render(request, "AppCoder/listaScores.html", 
                #{"listaWods": listaWods}, 
                #{"listaAtletas": listaAtletas}
                )
    else:
        miFormulario = ScoreFormulario()

    return render(request, "AppCoder/crearScore.html", {"formulario1":miFormulario})

 