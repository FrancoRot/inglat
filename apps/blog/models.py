# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField
from .utils import VideoURLValidator, validate_public_video_url, clean_video_url
import re
import os
import logging


def validate_multimedia_file(archivo):
    """Validador personalizado para archivos multimedia"""
    if not archivo:
        return
    
    # Obtener extensión del archivo
    ext = os.path.splitext(archivo.name)[1].lower()
    
    # Extensiones permitidas
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    video_extensions = ['.mp4', '.webm', '.mov', '.avi', '.m4v']
    
    if ext not in image_extensions + video_extensions:
        raise ValidationError(
            f'Tipo de archivo no soportado: {ext}. '
            f'Extensiones permitidas: {", ".join(image_extensions + video_extensions)}'
        )


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
        indexes = [
            # Índice para categorías activas (usado en queries de filtro)
            models.Index(fields=['activa', 'orden'], name='blog_categoria_activa_orden'),
        ]
    
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
        ('video', 'Video'),
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
    archivo = models.FileField(
        upload_to='noticias/archivos/', 
        blank=True, 
        null=True,
        validators=[validate_multimedia_file],
        help_text="Archivo multimedia: JPG/PNG para imagenes o MP4/WebM/MOV para videos"
    )
    
    # Miniatura personalizada
    thumbnail_custom = models.ImageField(
        upload_to='noticias/thumbnails/',
        blank=True,
        null=True,
        help_text="Miniatura personalizada para mostrar en las tarjetas (opcional)"
    )
    
    # Sistema multimedia universal por URL (renombrado de video_url)
    video_url = models.URLField(
        blank=True,
        help_text=(
            "URL publica de imagen o video. Soportamos: YouTube, Vimeo, Google Drive, "
            "Dropbox, URLs directas de imagenes (JPG/PNG) o videos (MP4). "
            "Ejemplo: https://www.youtube.com/watch?v=abc123"
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
        default=True,
        help_text="Reproducir automaticamente en la vista detalle"
    )
    video_muted = models.BooleanField(
        default=True,
        help_text="Silenciar video por defecto"
    )
    video_loop = models.BooleanField(
        default=True,
        help_text="Reproducir video en bucle infinito"
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
        indexes = [
            # Índice para queries de noticias activas (más común)
            models.Index(fields=['activa', '-fecha_publicacion'], name='blog_noticia_activa_fecha'),
            # Índice para noticias destacadas
            models.Index(fields=['destacada', 'activa'], name='blog_noticia_destacada'),
            # Índice para filtros por autor (EstefaniPUBLI)
            models.Index(fields=['autor', 'activa'], name='blog_noticia_autor'),
            # Índice para filtros por categoría
            models.Index(fields=['categoria', 'activa', '-fecha_publicacion'], name='blog_noticia_categoria'),
            # Índice compuesto para la query más común: activa + categoria + fecha
            models.Index(fields=['activa', 'categoria', '-fecha_publicacion'], name='blog_noticia_main_query'),
        ]
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        # Generar slug automaticamente si no existe
        if not self.slug:
            self.slug = slugify(self.titulo)
        
        # Procesar URL multimedia universal
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
    def archivo_url(self):
        """Retorna la URL del archivo (imagen o video) o None"""
        if self.archivo:
            return self.archivo.url
        return None
    
    @property
    def imagen_url(self):
        """Retorna la URL de la imagen o None (backward compatibility)"""
        if self.archivo and self.tipo_multimedia == 'imagen':
            return self.archivo.url
        return None
    
    @property
    def video_embed_url(self):
        """Retorna la URL para embebido del video (sistema universal)"""
        # Usar URL cacheada si existe
        if self.video_embed_url_cached:
            return self.video_embed_url_cached
        
        # Generar dinámicamente si hay URL multimedia
        if self.video_url:
            return VideoURLValidator.get_embed_url(self.video_url, self.video_platform)
        
        # Fallback a sistema legacy de Vimeo
        if self.video_vimeo_id:
            return f"https://player.vimeo.com/video/{self.video_vimeo_id}"
        
        return None
    
    @property
    def has_video(self):
        """Verifica si la noticia tiene video"""
        return bool(
            (self.tipo_multimedia == 'video' and self.archivo) or 
            self.video_url or 
            self.video_vimeo_url
        )
    
    @property
    def has_image(self):
        """Verifica si la noticia tiene imagen"""
        return bool(self.tipo_multimedia == 'imagen' and self.archivo)
    
    @property
    def multimedia_url(self):
        """Retorna la URL del multimedia principal (imagen o video)"""
        if self.tipo_multimedia == 'video' and self.has_video:
            return self.video_thumbnail_url or self.video_embed_url
        elif self.tipo_multimedia == 'imagen' and self.has_image:
            return self.archivo_url
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
        
        # Fallback a archivo si existe
        if self.archivo:
            return self.archivo.url
        
        return '/static/images/video-placeholder.jpg'
    
    def get_thumbnail_url(self):
        """Obtiene la miniatura con lógica de prioridades para tarjetas"""
        # Prioridad 1: Miniatura personalizada
        if self.thumbnail_custom:
            return self.thumbnail_custom.url
        
        # Prioridad 2: Frame automático de video si es MP4 local
        if self.tipo_multimedia == 'video' and self.archivo:
            # Para videos locales, usar el primer frame (esto requeriría procesamiento adicional)
            # Por ahora usamos el archivo como fallback
            return self.archivo.url
        
        # Prioridad 3: Thumbnail de URL externa de video
        if self.tipo_multimedia == 'video' and self.video_thumbnail_url:
            return self.video_thumbnail_url
        
        # Prioridad 4: Imagen original si tipo=imagen
        if self.tipo_multimedia == 'imagen' and self.archivo:
            return self.archivo.url
        
        # Fallback por defecto
        return None
    
    def get_noticias_relacionadas(self, limit=3):
        """Retorna noticias relacionadas de la misma categoria"""
        return Noticia.objects.filter(
            categoria=self.categoria,
            activa=True
        ).exclude(pk=self.pk)[:limit]
    
    def delete(self, *args, **kwargs):
        """Override delete para limpiar archivos de imagen asociados"""
        logger = logging.getLogger('estefani.cleanup')
        
        # Lista de archivos a eliminar
        archivos_a_eliminar = []
        
        # Si tiene archivo multimedia (imagen o video), agregarlo
        if self.archivo and hasattr(self.archivo, 'path'):
            try:
                if os.path.exists(self.archivo.path):
                    archivos_a_eliminar.append(self.archivo.path)
                    logger.info(f'Marcado para eliminar archivo multimedia: {self.archivo.path}')
            except ValueError:
                # El archivo ya no existe o path inválido
                pass
        
        # Si tiene miniatura personalizada, agregarla
        if self.thumbnail_custom and hasattr(self.thumbnail_custom, 'path'):
            try:
                if os.path.exists(self.thumbnail_custom.path):
                    archivos_a_eliminar.append(self.thumbnail_custom.path)
                    logger.info(f'Marcado para eliminar miniatura personalizada: {self.thumbnail_custom.path}')
            except ValueError:
                # El archivo ya no existe o path inválido
                pass
        
        # Buscar imágenes generadas por EstefaniPUBLI asociadas a esta noticia
        # Patrón: titulo_timestamp_source.jpg
        if self.titulo:
            import glob
            from django.conf import settings
            
            # Generar posibles patrones de nombres de archivo
            titulo_limpio = ''.join(c for c in self.titulo.lower() if c.isalnum() or c.isspace()).replace(' ', '_')[:30]
            patron_busqueda = os.path.join(
                settings.MEDIA_ROOT, 
                'noticias', 
                'imagenes',
                f"{titulo_limpio}_*.*"
            )
            
            # Buscar también archivos de video y thumbnails asociados
            patron_videos = os.path.join(
                settings.MEDIA_ROOT, 
                'noticias', 
                'archivos',
                f"{titulo_limpio}_*.*"
            )
            patron_thumbnails = os.path.join(
                settings.MEDIA_ROOT, 
                'noticias', 
                'thumbnails',
                f"{titulo_limpio}_*.*"
            )
            
            archivos_encontrados = glob.glob(patron_busqueda)
            videos_encontrados = glob.glob(patron_videos)
            thumbnails_encontrados = glob.glob(patron_thumbnails)
            
            archivos_a_eliminar.extend(archivos_encontrados)
            archivos_a_eliminar.extend(videos_encontrados)
            archivos_a_eliminar.extend(thumbnails_encontrados)
            
            total_archivos = len(archivos_encontrados) + len(videos_encontrados) + len(thumbnails_encontrados)
            if total_archivos > 0:
                logger.info(f'Encontrados {total_archivos} archivos EstefaniPUBLI para eliminar (imágenes: {len(archivos_encontrados)}, videos: {len(videos_encontrados)}, thumbnails: {len(thumbnails_encontrados)})')
        
        # Eliminar la noticia de la base de datos primero
        super().delete(*args, **kwargs)
        
        # Ahora eliminar los archivos físicos
        archivos_eliminados = 0
        for archivo_path in archivos_a_eliminar:
            try:
                if os.path.exists(archivo_path):
                    os.remove(archivo_path)
                    archivos_eliminados += 1
                    logger.info(f'Archivo eliminado: {archivo_path}')
            except OSError as e:
                logger.error(f'Error eliminando archivo {archivo_path}: {str(e)}')
        
        if archivos_eliminados > 0:
            logger.info(f'Limpieza completada: {archivos_eliminados} archivos eliminados para noticia "{self.titulo}"')
        else:
            logger.info(f'Sin archivos que limpiar para noticia "{self.titulo}"')