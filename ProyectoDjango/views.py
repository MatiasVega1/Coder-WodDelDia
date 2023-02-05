from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.shortcuts import render, redirect

# Redirigir a mi pagina principal siempre que inicie la aplicación
def default(request):
    return render(request, "AppCoder/inicio.html")  