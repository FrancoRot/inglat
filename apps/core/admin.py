# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Configuracion del panel de administracion para Proyectos"""
    
    list_display = [
        'title', 
        'location', 
        'date_completed', 
        'power_capacity',
        'client_type',
        'is_featured', 
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'is_featured', 
        'is_active',
        'client_type',
        'date_completed',
        'created_at'
    ]
    
    search_fields = [
        'title', 
        'location', 
        'description_short',
        'client_type',
        'power_capacity'
    ]
    
    list_editable = [
        'is_featured', 
        'is_active'
    ]
    
    prepopulated_fields = {
        'slug': ('title',)
    }
    
    fieldsets = (
        ('Informacion Principal', {
            'fields': ('title', 'slug', 'location', 'date_completed')
        }),
        ('Descripcion', {
            'fields': ('description_short', 'description_full')
        }),
        ('Detalles Tecnicos', {
            'fields': ('power_capacity', 'client_type')
        }),
        ('Imagen', {
            'fields': ('featured_image',)
        }),
        ('Configuracion', {
            'fields': ('is_featured', 'is_active'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    ordering = ['-date_completed', '-created_at']
    
    # Configuracion de la vista de lista
    list_per_page = 20
    date_hierarchy = 'date_completed'
    
    # Configuracion de formularios
    save_on_top = True
    
    def get_queryset(self, request):
        """Optimizar las consultas para el listado del admin"""
        return super().get_queryset(request).select_related()
    
    class Media:
        css = {
            'all': ('admin/css/custom-project-admin.css',)
        }
        js = ('admin/js/custom-project-admin.js',)