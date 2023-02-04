from django.shortcuts import render, redirect
from django.http import HttpResponse
from AppCoder.models import *
from AppCoder.forms import *
 
from .models import Task
from .forms import ValueListForm
from .models import ValueList
from .forms import FormularioPrincipalForm, FormularioForm

# Paginas de Inicio
def inicio(request):
    return render(request, "AppCoder/inicio.html")

# ABM de Atletas
def verAtletas(request):
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

def buscarAtleta(request):
    return render(request, "AppCoder/buscarAtleta.html")

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
def verWods(request):
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

def buscarWod(request):
    return render(request, "AppCoder/buscarWod.html")

def verWod(request):
    if request.GET["tipo"]:

        tipo = request.GET['tipo'] 
        
        wod1 = Wod.objects.filter(tipo__icontains= tipo)
        return render(request, "AppCoder/verAtleta.html", { "wod": wod1, 
                                                            "tipo": tipo})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta)


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'AppCoder/task_list.html', {'tasks': tasks})




# ABM de Movimientos
def verMovimientos(request):
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

def buscarMovimiento(request):
    return render(request, "AppCoder/buscarMovimiento.html")

def verMovimiento(request):
    if request.GET["tipo"]:

        tipo = request.GET['tipo'] 
        
        mov1 = Movimiento.objects.filter(tipo__icontains= tipo)
        return render(request, "AppCoder/verMovimiento.html", { "movimiento": mov1, 
                                                            "tipo": tipo})
    else:
        respuesta = "No enviaste datos"
    
    return HttpResponse(respuesta)



def crearScore(request):
    if request.method == 'POST':
        
        miFormulario = ScoreFormulario(request.POST)

        if miFormulario.is_valid():
            infoDic = miFormulario.cleaned_data # La info formulario pasa a diccionario

            sco1 = Score(   fecha = infoDic["fecha"],  
                            score = infoDic["score"])

   
            sco1.save() 
            
            listaWods = Wod.objects.all() 
            listaAtletas = Wod.objects.all() 

            return render(request, "AppCoder/listaMovimientos.html", 
                {"listaWods": listaWods}, 
                {"listaAtletas": listaAtletas})
    else:
        miFormulario = ScoreFormulario()

    return render(request, "AppCoder/crearScore.html", {"formulario1":miFormulario})





def value_list_view(request):
    #value_lists = ValueList.objects.all()
    
    if request.method == "POST":
        print("Aca")
        form = ValueListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("value_list")
    else:
        form = ValueListForm()
    return render(request, "AppCoder/value_list.html", {"form": form})



def formulario_view(request):
    if request.method == 'POST':
        form = FormularioForm(request.POST)
        if form.is_valid():
            form.save()
            # Aquí puedes agregar la lógica adicional para procesar el formulario
    else:
        form = FormularioForm()
    return render(request, 'AppCoder/value_list.html', {'form': form})


def formulario_principal_view(request):
    formulario_form = FormularioForm()
    if request.method == 'POST':
        form = FormularioPrincipalForm(request.POST)
        if form.is_valid():
            form.save()
            # Aquí puedes agregar la lógica adicional para procesar el formulario
    else:
        form = FormularioPrincipalForm()
    return render(request, 'AppCoder/formulario_principal.html', {'form': form, 'formulario_form': formulario_form})