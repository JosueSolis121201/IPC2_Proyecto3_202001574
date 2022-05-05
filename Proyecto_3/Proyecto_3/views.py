from re import template
from unittest import loader
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import requests

def home (request):
    template =loader.get_template("pagina.html")
    respuesta = requests.get("http://127.0.0.1:5000/estudiante")
    context= respuesta.json()


    if(request.GET.get('cargar')):
      lectura = {"texto": request.GET.get("entrada")}
      estado = requests.post("http://127.0.0.1:5000/estudiante",json=lectura)
      context["nombre"] = estado.json()["texto"]

    
    return HttpResponse(template.render(context, request))
    


  #if(request.GET.get('mybtn')):
    #mypythoncode.mypythonfunction( int(request.GET.get('mytextbox')) )
    #return render(request,'myApp/templateHTML.html')