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
                'archivo',
                'video_url',
                'multimedia_preview',
                ('video_autoplay', 'video_muted', 'video_loop', 'video_show_controls'),
                'thumbnail_custom',
                'thumbnail_section'
            ),
            'description': 'Sube un archivo (imagen/video) O usa una URL, no ambos. Soportamos YouTube, Vimeo, Google Drive, Dropbox y URLs directas.',
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
        'fecha_actualizacion', 'multimedia_preview', 'thumbnail_section', 'video_options'
    ]
    
    def multimedia_preview(self, obj):
        """Muestra una preview del archivo o URL subida inmediatamente"""
        if not obj.pk:
            return format_html('<i style="color: #999;">Guarda la noticia para ver preview</i>')
        
        preview_html = '<div style="border: 1px solid #ddd; padding: 10px; border-radius: 4px; max-width: 300px;">'
        
        # Preview del archivo
        if obj.archivo:
            if obj.tipo_multimedia == 'imagen':
                preview_html += f'<h4>📁 Archivo (Imagen)</h4><img src="{obj.archivo.url}" style="max-width: 200px; max-height: 150px; border-radius: 4px;" />'
            elif obj.tipo_multimedia == 'video':
                preview_html += f'<h4>📁 Archivo (Video)</h4><video width="200" height="150" controls><source src="{obj.archivo.url}" type="video/mp4">Tu navegador no soporta video HTML5.</video>'
        
        # Preview de URL
        elif obj.video_url:
            if obj.video_thumbnail_url:
                preview_html += f'<h4>🔗 URL ({obj.video_platform.upper()})</h4><img src="{obj.video_thumbnail_url}" style="max-width: 200px; max-height: 150px; border-radius: 4px;" />'
            else:
                preview_html += f'<h4>🔗 URL ({obj.video_platform.upper() if obj.video_platform else "Desconocida"})</h4><p>URL: {obj.video_url[:50]}...</p>'
        
        # Si no hay contenido
        else:
            preview_html += '<p style="color: #666;"><i>Sin contenido multimedia</i></p>'
        
        preview_html += '</div>'
        return format_html(preview_html)
    multimedia_preview.short_description = 'Previsualización'
    
    def thumbnail_section(self, obj):
        """Muestra la sección de miniatura con preview y opciones"""
        if not obj.pk:
            return format_html('<i style="color: #999;">Guarda la noticia para configurar miniatura</i>')
        
        thumbnail_html = '<div style="border: 1px solid #ddd; padding: 10px; border-radius: 4px;">'
        
        # Mostrar miniatura actual
        current_thumbnail = obj.get_thumbnail_url()
        if current_thumbnail:
            thumbnail_html += f'<h4>🖼️ Miniatura actual:</h4><img src="{current_thumbnail}" style="max-width: 150px; max-height: 100px; border-radius: 4px; border: 2px solid #006466;" /><br><br>'
        
        # Mostrar qué se está usando como miniatura
        if obj.thumbnail_custom:
            thumbnail_html += '✅ <strong>Usando miniatura personalizada</strong>'
        elif obj.tipo_multimedia == 'video' and obj.archivo:
            thumbnail_html += '🎬 Usando frame de video local'
        elif obj.tipo_multimedia == 'video' and obj.video_thumbnail_url:
            thumbnail_html += '🔗 Usando thumbnail de URL externa'
        elif obj.tipo_multimedia == 'imagen' and obj.archivo:
            thumbnail_html += '🖼️ Usando imagen original'
        else:
            thumbnail_html += '⚠️ Sin miniatura disponible'
        
        thumbnail_html += '</div>'
        return format_html(thumbnail_html)
    thumbnail_section.short_description = 'Miniatura para Tarjetas'
    
    def video_options(self, obj):
        """Muestra las opciones de video cuando aplica"""
        if obj.tipo_multimedia != 'video':
            return format_html('<i style="color: #666;">Solo disponible para videos</i>')
        
        options_html = '<div style="border: 1px solid #ddd; padding: 10px; border-radius: 4px;">'
        options_html += '<h4>🎛️ Configuración de Video:</h4>'
        options_html += f'<p>▶️ <strong>Autoplay:</strong> {"✅ Sí" if obj.video_autoplay else "❌ No"}</p>'
        options_html += f'<p>🔇 <strong>Muted:</strong> {"✅ Sí" if obj.video_muted else "❌ No"}</p>'
        options_html += f'<p>🔄 <strong>Loop:</strong> {"✅ Sí" if obj.video_loop else "❌ No"}</p>'
        options_html += f'<p>🎮 <strong>Controles:</strong> {"✅ Sí" if obj.video_show_controls else "❌ No"}</p>'
        options_html += '</div>'
        return format_html(options_html)
    video_options.short_description = 'Opciones de Video'
    
    def video_platform_info(self, obj):
        """Muestra información detallada del video"""
        if not obj.video_url:
            return format_html('<i>No hay URL multimedia configurada</i>')
        
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
        # Validar que no se use archivo y URL al mismo tiempo
        if obj.archivo and obj.video_url:
            # Priorizar archivo sobre URL
            obj.video_url = ''
        
        # Limpiar campos legacy si se está usando el nuevo sistema
        if obj.video_url and obj.video_vimeo_url:
            obj.video_vimeo_url = ''
            obj.video_vimeo_id = ''
        
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
            )
        }
        js = (
            'admin/js/multimedia_admin.js',
        )


# Personalizacion del admin header
admin.site.site_header = "INGLAT - Panel de Administracion"
admin.site.site_title = "INGLAT Admin"
admin.site.index_title = "Administracion de Contenido INGLAT"