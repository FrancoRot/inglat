from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from datetime import datetime
from .models import Project


class HomeView(TemplateView):
    """Vista principal de la página de inicio de INGLAT"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener proyectos destacados para mostrar en el home
        featured_projects = Project.objects.filter(
            is_featured=True, 
            is_active=True
        ).order_by('-date_completed')[:6]  # Máximo 6 proyectos destacados
        
        context.update({
            'current_year': datetime.now().year,
            'page_title': 'INGLAT - Líderes en Energía Renovable',
            'meta_description': 'INGLAT es líder en instalaciones de energía fotovoltaica y renovable. Especialistas en paneles solares, mantenimiento y monitorización en tiempo real.',
            'hero_title': 'Liderando la Transición Energética con Instalaciones Solares Inteligentes',
            'hero_subtitle': 'Monitorización avanzada, control total y soluciones a medida para tu independencia energética.',
            'featured_projects': featured_projects,
        })
        return context


def index(request):
    """Vista función para la página de inicio"""
    
    # Obtener proyectos destacados para mostrar en el home
    featured_projects = Project.objects.filter(
        is_featured=True, 
        is_active=True
    ).order_by('-date_completed')[:6]  # Máximo 6 proyectos destacados
    
    context = {
        'current_year': datetime.now().year,
        'page_title': 'INGLAT - Líderes en Energía Renovable',
        'meta_description': 'INGLAT es líder en instalaciones de energía fotovoltaica y renovable. Especialistas en paneles solares, mantenimiento y monitorización en tiempo real.',
        'hero_title': 'Liderando la Transición Energética con Instalaciones Solares Inteligentes',
        'hero_subtitle': 'Monitorización avanzada, control total y soluciones a medida para tu independencia energética.',
        'featured_projects': featured_projects,
    }
    return render(request, 'core/home.html', context)


class AboutView(TemplateView):
    """Vista de la página Nosotros"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_year': datetime.now().year,
            'page_title': 'Nosotros - INGLAT',
            'meta_description': 'Conoce más sobre INGLAT, empresa líder en instalaciones de energía renovable con años de experiencia en el sector fotovoltaico.',
        })
        return context


class ServicesView(TemplateView):
    """Vista de la página de Servicios"""
    template_name = 'core/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_year': datetime.now().year,
            'page_title': 'Servicios - INGLAT',
            'meta_description': 'Descubre nuestros servicios: instalación solar, mantenimiento, monitorización y consultoría energética. Soluciones integrales en energía renovable.',
        })
        return context