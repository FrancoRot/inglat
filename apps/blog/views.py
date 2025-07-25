from django.shortcuts import render
from django.http import HttpResponse

def blog_list(request):
    """Vista temporal para lista de blog"""
    return HttpResponse("<h1>Blog - Proximamente</h1><p>Esta seccion estara disponible proximamente.</p>")

def blog_detail(request, pk):
    """Vista temporal para detalle de post"""
    return HttpResponse(f"<h1>Post {pk} - Proximamente</h1><p>Esta seccion estara disponible proximamente.</p>")