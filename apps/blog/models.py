# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField
from .utils import VideoURLValidator, validate_public_video_url, clean_video_url
import re


class Categoria(models.Model):
    """Modelo para categorias del blog"""
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True, help_text="Descripcion breve de la categoria")
    icono = models.CharField(max_length=50, blank=True, help_text="Clase de icono FontAwesome (ej: fas fa-solar-panel)")
    color = models.CharField(max_length=7, default="#006466", help_text="Color en formato hex (ej: #006466)")
    orden = models.PositiveIntegerField(default=0, help_text="Orden de aparicion (menor numero = primero)")
    activa = models.BooleanField(default=True, help_text="Si esta marcada, la categoria aparece en el sitio")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:por_categoria', kwargs={'categoria_slug': self.slug})
    
    @property
    def noticias_count(self):
        return self.noticia_set.filter(activa=True).count()


class Noticia(models.Model):
    """Modelo principal para noticias del blog"""
    
    # Opciones para tipo de multimedia
    TIPO_MEDIA_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video de Vimeo'),
        ('ninguno', 'Sin multimedia')
    ]
    
    # Contenido principal
    titulo = models.CharField(max_length=200, help_text="Titulo de la noticia")
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    descripcion_corta = models.TextField(
        max_length=300, 
        help_text="Resumen que aparece en las tarjetas y como meta descripcion"
    )
    contenido = HTMLField(help_text="Contenido completo del articulo con formato rico")
    
    # Multimedia (IMAGEN O VIDEO - no ambos)
    tipo_multimedia = models.CharField(
        max_length=10, 
        choices=TIPO_MEDIA_CHOICES, 
        default='imagen',
        help_text="Selecciona el tipo de multimedia para el articulo"
    )
    imagen = models.ImageField(
        upload_to='noticias/imagenes/', 
        blank=True, 
        null=True,
        help_text="Imagen principal del articulo (JPG, PNG)"
    )
    
    # Sistema de video universal
    video_url = models.URLField(
        blank=True,
        help_text=(
            "URL publica de video. Soportamos: YouTube, Vimeo, Google Drive, "
            "Dropbox y URLs directas MP4. Ejemplo: https://www.youtube.com/watch?v=abc123"
        )
    )
    video_platform = models.CharField(
        max_length=20,
        blank=True,
        help_text="Plataforma de video (se detecta automaticamente)"
    )
    video_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="ID del video (se extrae automaticamente)"
    )
    video_embed_url_cached = models.URLField(
        blank=True,
        help_text="URL de embed cacheada (se genera automaticamente)"
    )
    video_thumbnail_url = models.URLField(
        blank=True,
        help_text="URL de thumbnail del video (se genera automaticamente)"
    )
    
    # Configuracion de video
    video_autoplay = models.BooleanField(
        default=False,
        help_text="Reproducir automaticamente en la vista detalle"
    )
    video_muted = models.BooleanField(
        default=True,
        help_text="Silenciar video por defecto"
    )
    video_show_controls = models.BooleanField(
        default=True,
        help_text="Mostrar controles de video"
    )
    
    # Campos legacy de Vimeo (mantener por compatibilidad)
    video_vimeo_url = models.URLField(
        blank=True, 
        help_text="DEPRECATED: Usar campo video_url. URL completa del video de Vimeo"
    )
    video_vimeo_id = models.CharField(
        max_length=20, 
        blank=True,
        help_text="DEPRECATED: Usar campo video_id. ID del video de Vimeo"
    )
    
    # Metadatos
    autor = models.CharField(max_length=100, default="Equipo INGLAT")
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True,
        help_text="Categoria de la noticia"
    )
    fecha_publicacion = models.DateTimeField(
        default=timezone.now,
        help_text="Fecha y hora de publicacion"
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_descripcion = models.CharField(
        max_length=160, 
        blank=True,
        help_text="Descripcion para motores de busqueda (max 160 caracteres)"
    )
    meta_keywords = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Palabras clave separadas por comas"
    )
    
    # Control
    destacada = models.BooleanField(
        default=False, 
        help_text="Si esta marcada, aparece en la pagina principal"
    )
    activa = models.BooleanField(
        default=True, 
        help_text="Si esta marcada, la noticia es visible en el sitio"
    )
    orden = models.PositiveIntegerField(
        default=0, 
        help_text="Orden manual (menor numero = mas arriba)"
    )
    
    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ['-fecha_publicacion', 'orden']
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        # Generar slug automaticamente si no existe
        if not self.slug:
            self.slug = slugify(self.titulo)
        
        # Procesar URL de video universal
        if self.video_url:
            self.video_url = clean_video_url(self.video_url)
            self.video_platform = VideoURLValidator.detect_platform(self.video_url)
            self.video_id = VideoURLValidator.extract_video_id(self.video_url, self.video_platform)
            self.video_embed_url_cached = VideoURLValidator.get_embed_url(self.video_url, self.video_platform)
            self.video_thumbnail_url = VideoURLValidator.get_thumbnail_url(self.video_url, self.video_platform) or ''
        else:
            # Limpiar campos de video si no hay URL
            self.video_platform = ''
            self.video_id = ''
            self.video_embed_url_cached = ''
            self.video_thumbnail_url = ''
        
        # Migrar datos legacy de Vimeo si existen
        if self.video_vimeo_url and not self.video_url:
            self.video_url = self.video_vimeo_url
            self.video_platform = 'vimeo'
            if self.video_vimeo_id:
                self.video_id = self.video_vimeo_id
            else:
                self.video_id = VideoURLValidator.extract_video_id(self.video_vimeo_url, 'vimeo')
            self.video_embed_url_cached = VideoURLValidator.get_embed_url(self.video_vimeo_url, 'vimeo')
        
        # Extraer ID de Vimeo automaticamente de la URL (legacy support)
        if self.video_vimeo_url and not self.video_vimeo_id:
            match = re.search(r'vimeo\.com/(\d+)', self.video_vimeo_url)
            if match:
                self.video_vimeo_id = match.group(1)
        
        # Si no hay meta_descripcion, usar descripcion_corta
        if not self.meta_descripcion and self.descripcion_corta:
            self.meta_descripcion = self.descripcion_corta[:160]
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:detalle', kwargs={'slug': self.slug})
    
    @property
    def fecha_formateada(self):
        """Retorna la fecha en formato legible"""
        return self.fecha_publicacion.strftime("%d de %B de %Y")
    
    @property
    def tiempo_lectura(self):
        """Estima el tiempo de lectura en minutos"""
        palabras = len(self.contenido.split())
        minutos = max(1, palabras // 200)  # Asumiendo 200 palabras por minuto
        return f"{minutos} min de lectura"
    
    @property
    def imagen_url(self):
        """Retorna la URL de la imagen o None"""
        if self.imagen:
            return self.imagen.url
        return None
    
    @property
    def video_embed_url(self):
        """Retorna la URL para embebido del video (sistema universal)"""
        # Usar URL cacheada si existe
        if self.video_embed_url_cached:
            return self.video_embed_url_cached
        
        # Generar dinámicamente si hay URL de video
        if self.video_url:
            return VideoURLValidator.get_embed_url(self.video_url, self.video_platform)
        
        # Fallback a sistema legacy de Vimeo
        if self.video_vimeo_id:
            return f"https://player.vimeo.com/video/{self.video_vimeo_id}"
        
        return None
    
    @property
    def has_video(self):
        """Verifica si la noticia tiene video"""
        return bool(self.video_url or self.video_vimeo_url)
    
    @property
    def has_image(self):
        """Verifica si la noticia tiene imagen"""
        return bool(self.imagen)
    
    @property
    def multimedia_url(self):
        """Retorna la URL del multimedia principal (imagen o video)"""
        if self.tipo_multimedia == 'video' and self.has_video:
            return self.video_thumbnail_url or self.video_embed_url
        elif self.tipo_multimedia == 'imagen' and self.has_image:
            return self.imagen_url
        return None
    
    @property
    def multimedia_type(self):
        """Retorna el tipo de multimedia detectado automáticamente"""
        if self.has_video:
            return 'video'
        elif self.has_image:
            return 'image'
        return None
    
    def get_video_thumbnail(self):
        """Obtiene thumbnail del video con fallback a imagen"""
        if self.video_thumbnail_url:
            return self.video_thumbnail_url
        
        # Generar dinámicamente si no está cacheado
        if self.video_url:
            thumbnail = VideoURLValidator.get_thumbnail_url(self.video_url, self.video_platform)
            if thumbnail:
                return thumbnail
        
        # Fallback a imagen si existe
        if self.imagen:
            return self.imagen.url
        
        return '/static/images/video-placeholder.jpg'
    
    def get_noticias_relacionadas(self, limit=3):
        """Retorna noticias relacionadas de la misma categoria"""
        return Noticia.objects.filter(
            categoria=self.categoria,
            activa=True
        ).exclude(pk=self.pk)[:limit]