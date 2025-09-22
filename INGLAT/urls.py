"""
URL configuration for INGLAT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # TinyMCE URLs para el editor de texto rico
    path('tinymce/', include('tinymce.urls')),
    
    # URLs de la aplicación core (página principal)
    path('', include('apps.core.urls')),
    
    # URLs para otras aplicaciones
    path('proyectos/', include('apps.projects.urls')),
    path('noticias/', include('apps.blog.urls')),
    path('contacto/', include('apps.contact.urls')),
    
    # Redirecciones de compatibilidad para URLs antiguas
    path('blog/', lambda request: redirect('/noticias/', permanent=True)),
    path('blog/<path:path>', lambda request, path: redirect(f'/noticias/{path}', permanent=True)),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
