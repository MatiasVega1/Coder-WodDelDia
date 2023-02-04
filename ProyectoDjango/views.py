from django.http import HttpResponse
import datetime
from django.template import Template, Context

def saludo(request, nombre):
    horaActual = datetime.datetime.now()
    return HttpResponse(f"Hola mundo! {horaActual} {nombre}")

def miNombre(request):
    return HttpResponse("Hola me llamo mati")

def miPagina(request):

    diccionario = {"nombre": "Matias"}
    miHtml = open("C:/Users/Usuario/Python/ProyectoDjango/ProyectoDjango/plantillas/prueba.html")
    
    plantilla = Template(miHtml.read())

    miHtml.close()

    miContexto = Context(diccionario)

    documento = plantilla.render(miContexto)

    return HttpResponse(documento)