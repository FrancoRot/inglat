# -*- coding: utf-8 -*-
"""
Configuración personalizada del admin panel para organizar modelos en grupos
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html


class CustomAdminSite(AdminSite):
    """Sitio de administración personalizado con grupos organizados"""
    
    site_header = 'INGLAT - Panel de Administración'
    site_title = 'INGLAT Admin'
    index_title = 'Administración de Contenido INGLAT'
    
    def index(self, request, extra_context=None):
        """
        Personalizar la página de inicio del admin con grupos organizados
        """
        extra_context = extra_context or {}
        
        # Definir grupos de aplicaciones personalizados
        app_groups = {
            'home': {
                'name': 'Home - Portada',
                'icon': 'fas fa-home',
                'color': '#4CAF50',
                'models': [
                    ('core', 'homeportada'),
                    ('core', 'project'),
                ],
                'description': 'Gestión del contenido de la portada principal y proyectos destacados'
            },
            'simulador': {
                'name': 'Simulador Solar',
                'icon': 'fas fa-solar-panel',
                'color': '#FF9800',
                'models': [
                    ('core', 'simuladorconfig'),
                    ('core', 'costoinstalacion'),
                    ('core', 'factorubicacion'),
                    ('core', 'factororientacion'),
                    ('core', 'tipotejado'),
                    ('core', 'angulotejado'),
                ],
                'description': 'Configuración y parámetros del simulador de energía solar'
            },
            'blog': {
                'name': 'Blog y Noticias',
                'icon': 'fas fa-newspaper',
                'color': '#2196F3',
                'models': [
                    ('blog', 'categoria'),
                    ('blog', 'noticia'),
                ],
                'description': 'Gestión de categorías y noticias del blog'
            },
            'contacto': {
                'name': 'Contacto y Comunicación',
                'icon': 'fas fa-envelope',
                'color': '#9C27B0',
                'models': [
                    ('contact', 'contactmessage'),
                ],
                'description': 'Mensajes de contacto y comunicación con clientes'
            },
            'usuarios': {
                'name': 'Usuarios y Permisos',
                'icon': 'fas fa-users',
                'color': '#607D8B',
                'models': [
                    ('auth', 'user'),
                    ('auth', 'group'),
                ],
                'description': 'Gestión de usuarios y permisos del sistema'
            }
        }
        
        extra_context['app_groups'] = app_groups
        
        return super().index(request, extra_context)
    
    def get_app_list(self, request, app_label=None):
        """
        Personalizar la lista de aplicaciones para organizarlas en grupos
        """
        app_dict = self._build_app_dict(request, app_label)
        
        # Reorganizar aplicaciones según nuestros grupos
        organized_apps = []
        
        # Grupo Home
        home_models = []
        if 'core' in app_dict:
            for model in app_dict['core']['models']:
                if model['object_name'].lower() in ['homeportada', 'project']:
                    home_models.append(model)
        
        if home_models:
            organized_apps.append({
                'name': 'Home - Portada',
                'app_label': 'home_group',
                'app_url': '',
                'has_module_perms': True,
                'models': home_models
            })
        
        # Grupo Simulador
        simulador_models = []
        if 'core' in app_dict:
            for model in app_dict['core']['models']:
                if model['object_name'].lower() in [
                    'simuladorconfig', 'costoinstalacion', 'factorubicacion', 
                    'factororientacion', 'tipotejado', 'angulotejado'
                ]:
                    simulador_models.append(model)
        
        if simulador_models:
            organized_apps.append({
                'name': 'Simulador Solar',
                'app_label': 'simulador_group',
                'app_url': '',
                'has_module_perms': True,
                'models': simulador_models
            })
        
        # Grupo Blog
        if 'blog' in app_dict:
            organized_apps.append({
                'name': 'Blog y Noticias',
                'app_label': 'blog',
                'app_url': app_dict['blog']['app_url'],
                'has_module_perms': app_dict['blog']['has_module_perms'],
                'models': app_dict['blog']['models']
            })
        
        # Grupo Contacto
        if 'contact' in app_dict:
            organized_apps.append({
                'name': 'Contacto y Comunicación',
                'app_label': 'contact',
                'app_url': app_dict['contact']['app_url'],
                'has_module_perms': app_dict['contact']['has_module_perms'],
                'models': app_dict['contact']['models']
            })
        
        # Usuarios y permisos
        if 'auth' in app_dict:
            organized_apps.append({
                'name': 'Usuarios y Permisos',
                'app_label': 'auth',
                'app_url': app_dict['auth']['app_url'],
                'has_module_perms': app_dict['auth']['has_module_perms'],
                'models': app_dict['auth']['models']
            })
        
        # Agregar cualquier otra app que no hayamos categorizado
        for app_name, app_data in app_dict.items():
            if app_name not in ['core', 'blog', 'contact', 'auth']:
                organized_apps.append(app_data)
        
        return organized_apps


# Crear instancia personalizada del admin
custom_admin_site = CustomAdminSite(name='custom_admin')