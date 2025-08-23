# -*- coding: utf-8 -*-
"""
Filtros personalizados para el blog de INGLAT
"""
from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter
def split(value, delimiter=','):
    """
    Divide una cadena por el delimitador especificado
    Uso: {{ meta_keywords|split:"," }}
    """
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter) if item.strip()]


@register.filter
def trim(value):
    """
    Elimina espacios en blanco al inicio y final de una cadena
    Uso: {{ keyword|trim }}
    """
    if not value:
        return ''
    return str(value).strip()


@register.filter
def truncate_smart(value, length=100):
    """
    Trunca texto de manera inteligente, cortando por palabras
    Uso: {{ descripcion|truncate_smart:150 }}
    """
    if not value:
        return ''
    
    value = str(value)
    if len(value) <= length:
        return value
    
    # Buscar el último espacio antes del límite
    truncated = value[:length]
    last_space = truncated.rfind(' ')
    
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return f"{truncated}..."


@register.filter
def extract_video_id(url, platform='youtube'):
    """
    Extrae el ID de video de diferentes plataformas
    Uso: {{ video_url|extract_video_id:"youtube" }}
    """
    if not url:
        return ''
    
    url = str(url)
    
    if platform == 'youtube':
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/embed/([a-zA-Z0-9_-]{11})'
        ]
    elif platform == 'vimeo':
        patterns = [
            r'vimeo\.com/(?:video/)?(\d+)',
            r'player\.vimeo\.com/video/(\d+)'
        ]
    else:
        return ''
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return ''


@register.filter
def is_video_url(url):
    """
    Verifica si una URL es de video
    Uso: {% if video_url|is_video_url %}
    """
    if not url:
        return False
    
    url = str(url).lower()
    video_domains = [
        'youtube.com', 'youtu.be', 'vimeo.com', 
        'drive.google.com', 'dropbox.com'
    ]
    video_extensions = ['.mp4', '.webm', '.ogg', '.avi', '.mov']
    
    # Verificar dominios de video
    for domain in video_domains:
        if domain in url:
            return True
    
    # Verificar extensiones de video
    for ext in video_extensions:
        if url.endswith(ext):
            return True
    
    return False


@register.filter
def video_platform(url):
    """
    Detecta la plataforma de video
    Uso: {{ video_url|video_platform }}
    """
    if not url:
        return 'unknown'
    
    url = str(url).lower()
    
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'vimeo.com' in url:
        return 'vimeo'
    elif 'drive.google.com' in url:
        return 'gdrive'
    elif 'dropbox.com' in url:
        return 'dropbox'
    elif url.endswith(('.mp4', '.webm', '.ogg')):
        return 'direct'
    
    return 'unknown'


@register.filter
def embed_url(url):
    """
    Convierte URLs de video a formato embed
    Uso: {{ video_url|embed_url }}
    """
    if not url:
        return ''
    
    url = str(url)
    platform = video_platform(url)
    
    if platform == 'youtube':
        video_id = extract_video_id(url, 'youtube')
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
    
    elif platform == 'vimeo':
        video_id = extract_video_id(url, 'vimeo')
        if video_id:
            return f"https://player.vimeo.com/video/{video_id}"
    
    elif platform == 'gdrive':
        # Convertir URL de Google Drive a formato directo
        file_id_match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
        if file_id_match:
            file_id = file_id_match.group(1)
            return f"https://drive.google.com/uc?export=download&id={file_id}"
    
    elif platform == 'dropbox':
        # Convertir URL de Dropbox a formato directo
        if '?dl=0' in url:
            return url.replace('?dl=0', '?dl=1')
    
    elif platform == 'direct':
        return url
    
    return url


@register.simple_tag
def video_thumbnail(url):
    """
    Genera URL de thumbnail para videos
    Uso: {% video_thumbnail video_url %}
    """
    if not url:
        return ''
    
    platform = video_platform(url)
    
    if platform == 'youtube':
        video_id = extract_video_id(url, 'youtube')
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    
    elif platform == 'vimeo':
        # Para Vimeo necesitaríamos hacer una API call
        # Por ahora retornamos placeholder
        return '/static/images/video-placeholder.jpg'
    
    return '/static/images/video-placeholder.jpg'


@register.inclusion_tag('blog/components/video_player.html')
def render_video(url, title='', autoplay=False, muted=True, controls=True):
    """
    Renderiza un video player responsivo
    Uso: {% render_video video_url title autoplay=False %}
    """
    if not url:
        return {'has_video': False}
    
    platform = video_platform(url)
    embed_video_url = embed_url(url)
    
    return {
        'has_video': True,
        'video_url': url,
        'embed_url': embed_video_url,
        'platform': platform,
        'title': title,
        'autoplay': autoplay,
        'muted': muted,
        'controls': controls,
        'video_id': extract_video_id(url, platform) if platform in ['youtube', 'vimeo'] else None
    }