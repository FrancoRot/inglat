# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django import forms
from tinymce.widgets import TinyMCE
from .models import Categoria, Noticia
from .utils import VideoURLValidator


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin interface para categorias del blog"""
    
    list_display = [
        'nombre', 
        'color_preview', 
        'icono_preview', 
        'noticias_count_display', 
        'activa', 
        'orden', 
        'created_at'
    ]
    list_filter = ['activa', 'created_at']
    search_fields = ['nombre', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ['orden', 'activa']
    ordering = ['orden', 'nombre']
    
    fieldsets = (
        ('Informacion Basica', {
            'fields': ('nombre', 'slug', 'descripcion')
        }),
        ('Apariencia', {
            'fields': ('icono', 'color'),
            'description': 'Icono FontAwesome (ej: fas fa-solar-panel) y color en formato hex'
        }),
        ('Control', {
            'fields': ('orden', 'activa')
        })
    )
    
    def color_preview(self, obj):
        """Muestra una preview del color"""
        if obj.color:
            return format_html(
                '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
                obj.color
            )
        return '-'
    color_preview.short_description = 'Color'
    
    def icono_preview(self, obj):
        """Muestra una preview del icono"""
        if obj.icono:
            return format_html(
                '<i class="{} fa-lg" style="color: {};"></i>',
                obj.icono,
                obj.color or '#333'
            )
        return '-'
    icono_preview.short_description = 'Icono'
    
    def noticias_count_display(self, obj):
        """Muestra la cantidad de noticias activas"""
        count = obj.noticias_count
        if count > 0:
            url = reverse('admin:blog_noticia_changelist') + f'?categoria__id__exact={obj.id}'
            return format_html('<a href="{}">{} noticias</a>', url, count)
        return '0 noticias'
    noticias_count_display.short_description = 'Noticias'
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',)
        }


class NoticiaAdminForm(forms.ModelForm):
    """Formulario personalizado para el admin de noticias con TinyMCE"""
    
    class Meta:
        model = Noticia
        fields = '__all__'
        widgets = {
            'contenido': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    """Admin interface para noticias del blog con soporte multimedia universal"""
    
    form = NoticiaAdminForm
    
    list_display = [
        'titulo', 
        'categoria', 
        'autor', 
        'fecha_publicacion', 
        'multimedia_preview',
        'destacada', 
        'activa',
        'vista_previa_link'
    ]
    list_filter = [
        'categoria', 
        'destacada', 
        'activa', 
        'tipo_multimedia',
        'fecha_publicacion',
        'autor'
    ]
    search_fields = ['titulo', 'descripcion_corta', 'contenido', 'autor']
    prepopulated_fields = {'slug': ('titulo',)}
    list_editable = ['destacada', 'activa']
    date_hierarchy = 'fecha_publicacion'
    ordering = ['-fecha_publicacion']
    
    fieldsets = (
        ('Contenido Principal', {
            'fields': ('titulo', 'slug', 'descripcion_corta', 'contenido')
        }),
        ('Categoria y Autor', {
            'fields': ('categoria', 'autor')
        }),
        ('Multimedia Universal', {
            'fields': (
                'tipo_multimedia', 
                'imagen', 
                'video_url',
                ('video_autoplay', 'video_muted', 'video_show_controls'),
                'video_platform_info'
            ),
            'description': 'Selecciona imagen O video, no ambos. Soportamos YouTube, Vimeo, Google Drive, Dropbox y URLs directas.',
            'classes': ('collapse',)
        }),
        ('Video Legacy (Vimeo)', {
            'fields': ('video_vimeo_url', 'video_vimeo_id'),
            'description': 'Campos legacy para compatibilidad con videos existentes de Vimeo.',
            'classes': ('collapse',)
        }),
        ('Video Información Automática', {
            'fields': ('video_platform', 'video_id', 'video_embed_url_cached', 'video_thumbnail_url'),
            'description': 'Estos campos se generan automáticamente al guardar.',
            'classes': ('collapse',)
        }),
        ('SEO y Metadatos', {
            'fields': ('meta_descripcion', 'meta_keywords'),
            'classes': ('collapse',),
            'description': 'Optimizacion para motores de busqueda'
        }),
        ('Control de Publicacion', {
            'fields': ('fecha_publicacion', 'destacada', 'activa', 'orden'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = [
        'video_platform', 'video_id', 'video_embed_url_cached', 'video_thumbnail_url',
        'video_vimeo_id', 'fecha_actualizacion', 'video_platform_info'
    ]
    
    def multimedia_preview(self, obj):
        """Muestra una preview del multimedia universal sin iconos de plataforma"""
        if obj.tipo_multimedia == 'imagen' and obj.imagen:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.imagen.url
            )
        elif obj.tipo_multimedia == 'video':
            # Mostrar thumbnail si está disponible
            if obj.video_thumbnail_url:
                return format_html(
                    '<img src="{}" width="50" height="30" style="object-fit: cover; border-radius: 4px;" /><div style="font-size: 10px; color: #666; margin-top: 2px;">📹 Video</div>',
                    obj.video_thumbnail_url
                )
            # Si no hay thumbnail, mostrar solo indicador de video
            elif obj.video_url or obj.video_vimeo_id:
                return format_html(
                    '<div style="width: 50px; height: 30px; background: #f0f0f0; border-radius: 4px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-play" style="color: #666;"></i></div><div style="font-size: 10px; color: #666; margin-top: 2px;">📹 Video</div>'
                )
        
        return format_html('<i class="fas fa-times" style="color: #999;"></i>')
    multimedia_preview.short_description = 'Multimedia'
    
    def video_platform_info(self, obj):
        """Muestra información detallada del video"""
        if not obj.video_url:
            return format_html('<i>No hay video configurado</i>')
        
        info_html = f'<strong>Plataforma:</strong> {obj.video_platform.upper()}<br>'
        if obj.video_id:
            info_html += f'<strong>ID:</strong> {obj.video_id}<br>'
        if obj.video_embed_url_cached:
            info_html += f'<strong>Embed URL:</strong> <a href="{obj.video_embed_url_cached}" target="_blank">Ver</a><br>'
        if obj.video_thumbnail_url:
            info_html += f'<strong>Thumbnail:</strong> <a href="{obj.video_thumbnail_url}" target="_blank">Ver</a>'
        
        return format_html(info_html)
    video_platform_info.short_description = 'Info del Video'
    
    def vista_previa_link(self, obj):
        """Link para ver la noticia en el sitio"""
        if obj.pk and obj.activa:
            return format_html(
                '<a href="{}" target="_blank" class="button">Ver en sitio</a>',
                obj.get_absolute_url()
            )
        return '-'
    vista_previa_link.short_description = 'Vista Previa'
    
    def get_form(self, request, obj=None, **kwargs):
        """Personaliza el formulario del admin"""
        form = super().get_form(request, obj, **kwargs)
        
        # Anadir help text dinamico
        if 'descripcion_corta' in form.base_fields:
            form.base_fields['descripcion_corta'].help_text = (
                "Maximo 300 caracteres. Se usara como meta descripcion si no se especifica otra."
            )
        
        return form
    
    def save_model(self, request, obj, form, change):
        """Guarda el modelo con validaciones adicionales"""
        # Validar que no se seleccionen imagen y video a la vez
        if obj.tipo_multimedia == 'imagen' and obj.video_vimeo_url:
            obj.video_vimeo_url = ''
            obj.video_vimeo_id = ''
        elif obj.tipo_multimedia == 'video' and obj.imagen:
            # No eliminamos la imagen, pero la ignoramos
            pass
        
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
            )
        }
        js = (
            # Podriamos anadir JS personalizado para validaciones en tiempo real
        )


# Personalizacion del admin header
admin.site.site_header = "INGLAT - Panel de Administracion"
admin.site.site_title = "INGLAT Admin"
admin.site.index_title = "Administracion de Contenido INGLAT"