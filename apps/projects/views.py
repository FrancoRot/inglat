from django.shortcuts import render
from django.http import HttpResponse

def project_list(request):
    """Vista temporal para lista de proyectos"""
    return HttpResponse("<h1>Proyectos - Proximamente</h1><p>Esta seccion estara disponible proximamente.</p>")

def project_detail(request, pk):
    """Vista temporal para detalle de proyecto"""
    return HttpResponse(f"<h1>Proyecto {pk} - Proximamente</h1><p>Esta seccion estara disponible proximamente.</p>")