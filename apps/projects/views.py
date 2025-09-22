from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from apps.core.models import Project

def project_list(request):
    """Vista temporal para lista de proyectos"""
    return HttpResponse("<h1>Proyectos - Proximamente</h1><p>Esta seccion estara disponible proximamente.</p>")

def project_detail(request, slug):
    """Vista temporal para detalle de proyecto por slug"""
    project = get_object_or_404(Project, slug=slug, is_active=True)
    return HttpResponse(f"<h1>{project.title} - Proximamente</h1><p>Proyecto en {project.location} - Funcionalidad completa estara disponible proximamente.</p>")