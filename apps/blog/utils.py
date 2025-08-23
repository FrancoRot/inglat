# -*- coding: utf-8 -*-
"""
Utilidades para el blog de INGLAT
"""
import re
from urllib.parse import urlparse, parse_qs
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import logging

# Importar requests opcionalmente para verificación de accesibilidad
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

logger = logging.getLogger(__name__)


class VideoURLValidator:
    """Validador personalizado para URLs de video"""
    
    SUPPORTED_PLATFORMS = {
        'youtube': {
            'domains': ['youtube.com', 'youtu.be', 'm.youtube.com'],
            'patterns': [
                r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
                r'youtube\.com/embed/([a-zA-Z0-9_-]{11})'
            ]
        },
        'vimeo': {
            'domains': ['vimeo.com', 'player.vimeo.com'],
            'patterns': [
                r'vimeo\.com/(?:video/)?(\d+)',
                r'player\.vimeo\.com/video/(\d+)'
            ]
        },
        'gdrive': {
            'domains': ['drive.google.com'],
            'patterns': [
                r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
                r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)'
            ]
        },
        'dropbox': {
            'domains': ['dropbox.com', 'www.dropbox.com'],
            'patterns': [
                r'dropbox\.com/s/([a-zA-Z0-9_-]+)/.*\?dl='
            ]
        }
    }
    
    @classmethod
    def detect_platform(cls, url):
        """Detecta la plataforma de video de una URL"""
        if not url:
            return 'unknown'
        
        url_lower = url.lower()
        
        for platform, config in cls.SUPPORTED_PLATFORMS.items():
            for domain in config['domains']:
                if domain in url_lower:
                    return platform
        
        # Verificar si es URL directa de video
        if cls._is_direct_video_url(url):
            return 'direct'
        
        return 'unknown'
    
    @classmethod
    def _is_direct_video_url(cls, url):
        """Verifica si es una URL directa de video"""
        video_extensions = ['.mp4', '.webm', '.ogg', '.avi', '.mov', '.m4v']
        url_lower = url.lower()
        
        # Verificar extensión
        for ext in video_extensions:
            if ext in url_lower:
                return True
        
        # Verificar content-type si es posible (solo si requests está disponible)
        if HAS_REQUESTS:
            try:
                response = requests.head(url, timeout=5, allow_redirects=True)
                content_type = response.headers.get('content-type', '').lower()
                if 'video/' in content_type:
                    return True
            except:
                pass
        
        return False
    
    @classmethod
    def extract_video_id(cls, url, platform=None):
        """Extrae el ID de video de una URL"""
        if not url:
            return None
        
        if not platform:
            platform = cls.detect_platform(url)
        
        if platform not in cls.SUPPORTED_PLATFORMS:
            return None
        
        patterns = cls.SUPPORTED_PLATFORMS[platform]['patterns']
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    @classmethod
    def get_embed_url(cls, url, platform=None):
        """Convierte una URL de video a formato embed"""
        if not url:
            return None
        
        if not platform:
            platform = cls.detect_platform(url)
        
        video_id = cls.extract_video_id(url, platform)
        
        if platform == 'youtube' and video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        
        elif platform == 'vimeo' and video_id:
            return f"https://player.vimeo.com/video/{video_id}"
        
        elif platform == 'gdrive' and video_id:
            return f"https://drive.google.com/uc?export=download&id={video_id}"
        
        elif platform == 'dropbox':
            if '?dl=0' in url:
                return url.replace('?dl=0', '?dl=1')
            elif '?dl=' not in url:
                return url + '?dl=1'
        
        elif platform == 'direct':
            return url
        
        return url
    
    @classmethod
    def get_thumbnail_url(cls, url, platform=None):
        """Obtiene URL de thumbnail para un video"""
        if not platform:
            platform = cls.detect_platform(url)
        
        if platform == 'youtube':
            video_id = cls.extract_video_id(url, platform)
            if video_id:
                # Intentar thumbnail de alta resolución primero
                return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        elif platform == 'vimeo':
            video_id = cls.extract_video_id(url, platform)
            if video_id:
                # Para Vimeo necesitaríamos usar su API
                # Por ahora retornamos None para usar placeholder
                return None
        
        return None
    
    @classmethod
    def validate_video_url(cls, url):
        """Valida que una URL de video sea accesible y pública"""
        if not url:
            raise ValidationError("URL de video requerida")
        
        # Validar formato de URL básico
        url_validator = URLValidator()
        try:
            url_validator(url)
        except ValidationError:
            raise ValidationError("Formato de URL inválido")
        
        # Detectar plataforma
        platform = cls.detect_platform(url)
        
        if platform == 'unknown':
            raise ValidationError(
                "Plataforma de video no soportada. "
                "Soportamos: YouTube, Vimeo, Google Drive, Dropbox y URLs directas MP4."
            )
        
        # Validar que el video ID sea extraíble para plataformas que lo requieren
        if platform in ['youtube', 'vimeo', 'gdrive'] and not cls.extract_video_id(url, platform):
            raise ValidationError(f"No se pudo extraer ID de video de la URL de {platform.capitalize()}")
        
        return True
    
    @classmethod
    def test_video_accessibility(cls, url, platform=None):
        """Prueba si un video es accesible públicamente"""
        if not platform:
            platform = cls.detect_platform(url)
        
        embed_url = cls.get_embed_url(url, platform)
        
        try:
            if platform in ['gdrive', 'dropbox', 'direct'] and HAS_REQUESTS:
                # Para URLs directas, hacer HEAD request solo si requests está disponible
                response = requests.head(embed_url, timeout=10, allow_redirects=True)
                return response.status_code == 200
            
            elif platform in ['youtube', 'vimeo']:
                # Para plataformas de embed, verificar que el ID exista
                video_id = cls.extract_video_id(url, platform)
                return video_id is not None
            
            else:
                # Si no tenemos requests, asumir que la URL es válida si tiene formato correcto
                return embed_url is not None
        
        except Exception as e:
            logger.warning(f"No se pudo verificar accesibilidad del video {url}: {e}")
            return False
        
        return True


def validate_public_video_url(url):
    """
    Validador Django para URLs de video públicas
    """
    VideoURLValidator.validate_video_url(url)
    return True


def clean_video_url(url):
    """
    Limpia y normaliza una URL de video
    """
    if not url:
        return url
    
    url = url.strip()
    
    # Remover parámetros innecesarios de YouTube
    if 'youtube.com' in url:
        # Mantener solo el parámetro v
        if 'watch?v=' in url:
            video_id = VideoURLValidator.extract_video_id(url, 'youtube')
            if video_id:
                url = f"https://www.youtube.com/watch?v={video_id}"
    
    return url