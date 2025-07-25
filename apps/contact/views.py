from django.shortcuts import render
from django.http import HttpResponse

def contact(request):
    """Vista temporal para contacto"""
    return HttpResponse("<h1>Contacto - Proximamente</h1><p>Esta seccion estara disponible proximamente.</p>")