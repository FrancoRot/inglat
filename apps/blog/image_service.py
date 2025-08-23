# -*- coding: utf-8 -*-
"""
Servicio de imágenes automáticas para EstefaniPUBLI
Integra APIs de Pexels y Pixabay para búsqueda y descarga de imágenes
"""
import requests
import os
import logging
from typing import Optional, Dict, List
from urllib.parse import urljoin, urlparse
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import hashlib
import time
from PIL import Image
import io


class ImageService:
    """Servicio para búsqueda y descarga automática de imágenes"""
    
    def __init__(self):
        self.pexels_api_key = getattr(settings, 'PEXELS_API_KEY', '')
        self.pixabay_api_key = getattr(settings, 'PIXABAY_API_KEY', '')
        self.config = getattr(settings, 'IMAGE_SEARCH_CONFIG', {})
        self.logger = logging.getLogger('estefani.images')
        self.session = requests.Session()
        
        # Validación segura de API keys
        self._validate_api_keys()
        
        # Cache simple en memoria para evitar requests duplicados
        self._cache = {}
    
    def _validate_api_keys(self):
        """Valida la configuración de API keys de forma segura"""
        if not self.pexels_api_key:
            self.logger.warning('Pexels API key no configurada - servicio limitado')
        elif len(self.pexels_api_key) < 10:
            self.logger.warning('Pexels API key parece inválida - verificar configuración')
        else:
            self.logger.info(f'Pexels API key configurada correctamente (longitud: {len(self.pexels_api_key)})')
            
        if not self.pixabay_api_key:
            self.logger.warning('Pixabay API key no configurada - servicio limitado')
        elif len(self.pixabay_api_key) < 10:
            self.logger.warning('Pixabay API key parece inválida - verificar configuración')
        else:
            self.logger.info(f'Pixabay API key configurada correctamente (longitud: {len(self.pixabay_api_key)})')
    
    def generar_keywords_inteligentes(self, titulo: str, portal: str = '') -> List[str]:
        """Genera keywords optimizadas para búsqueda de imágenes"""
        # Keywords base por sector energético
        keywords_base = {
            'solar': ['solar panels', 'photovoltaic', 'renewable energy', 'solar farm'],
            'eólica': ['wind turbine', 'wind energy', 'wind farm', 'renewable energy'],
            'hidroeléctrica': ['hydroelectric', 'dam', 'water power', 'renewable energy'],
            'renovable': ['renewable energy', 'green energy', 'sustainable power', 'clean energy']
        }
        
        # Detectar sector principal
        titulo_lower = titulo.lower()
        keywords = []
        
        # Agregar keywords específicos por sector
        for sector, terms in keywords_base.items():
            if sector in titulo_lower:
                keywords.extend(terms)
                break
        else:
            # Default: energía renovable general
            keywords.extend(keywords_base['renovable'])
        
        # Agregar contexto geográfico
        if any(geo in titulo_lower for geo in ['argentina', 'latam', 'latinoamerica', 'sudamerica']):
            keywords.append('latin america energy')
        
        # Agregar contexto empresarial/industrial
        if any(biz in titulo_lower for biz in ['empresa', 'comercial', 'industrial', 'autoconsumo']):
            keywords.append('commercial solar installation')
        
        return keywords[:3]  # Limitar a 3 keywords más relevantes
    
    def buscar_imagen_pexels(self, keywords: List[str]) -> Optional[Dict]:
        """Busca imagen en Pexels API"""
        if not self.pexels_api_key:
            self.logger.warning('Pexels API key no configurada')
            return None
        
        try:
            # Crear query string
            query = ' '.join(keywords)
            cache_key = f'pexels_{hashlib.md5(query.encode()).hexdigest()}'
            
            # Verificar cache
            if cache_key in self._cache:
                return self._cache[cache_key]
            
            url = "https://api.pexels.com/v1/search"
            params = {
                'query': query,
                'per_page': self.config.get('max_images_per_search', 5),
                'orientation': self.config.get('preferred_orientation', 'landscape'),
                'size': 'large'
            }
            headers = {
                'Authorization': self.pexels_api_key
            }
            
            response = self.session.get(
                url, 
                params=params, 
                headers=headers, 
                timeout=self.config.get('timeout_seconds', 30)
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get('photos'):
                # Seleccionar mejor imagen
                for photo in data['photos']:
                    src = photo.get('src', {})
                    large_url = src.get('large') or src.get('original')
                    
                    if large_url and photo.get('width', 0) >= self.config.get('min_image_width', 800):
                        result = {
                            'url': large_url,
                            'width': photo.get('width'),
                            'height': photo.get('height'),
                            'photographer': photo.get('photographer'),
                            'source': 'pexels',
                            'alt': f"Imagen sobre {query}"
                        }
                        
                        # Guardar en cache
                        self._cache[cache_key] = result
                        return result
            
            return None
            
        except Exception as e:
            # Log seguro sin exponer API keys
            error_msg = str(e)
            if self.pexels_api_key and self.pexels_api_key in error_msg:
                error_msg = error_msg.replace(self.pexels_api_key, '[API_KEY_HIDDEN]')
            self.logger.error(f'Error buscando en Pexels: {error_msg}')
            return None
    
    def buscar_imagen_pixabay(self, keywords: List[str]) -> Optional[Dict]:
        """Busca imagen en Pixabay API como fallback"""
        if not self.pixabay_api_key:
            self.logger.warning('Pixabay API key no configurada')
            return None
        
        try:
            query = ' '.join(keywords)
            cache_key = f'pixabay_{hashlib.md5(query.encode()).hexdigest()}'
            
            if cache_key in self._cache:
                return self._cache[cache_key]
            
            url = "https://pixabay.com/api/"
            params = {
                'key': self.pixabay_api_key,
                'q': query,
                'image_type': 'photo',
                'orientation': self.config.get('preferred_orientation', 'horizontal'),
                'min_width': self.config.get('min_image_width', 800),
                'min_height': self.config.get('min_image_height', 600),
                'per_page': self.config.get('max_images_per_search', 5)
            }
            
            response = self.session.get(url, params=params, timeout=self.config.get('timeout_seconds', 30))
            response.raise_for_status()
            
            data = response.json()
            if data.get('hits'):
                # Seleccionar mejor imagen
                for hit in data['hits']:
                    large_url = hit.get('largeImageURL') or hit.get('webformatURL')
                    
                    if large_url:
                        result = {
                            'url': large_url,
                            'width': hit.get('imageWidth'),
                            'height': hit.get('imageHeight'),
                            'photographer': hit.get('user'),
                            'source': 'pixabay',
                            'alt': f"Imagen sobre {query}"
                        }
                        
                        self._cache[cache_key] = result
                        return result
            
            return None
            
        except Exception as e:
            # Log seguro sin exponer API keys
            error_msg = str(e)
            if self.pixabay_api_key and self.pixabay_api_key in error_msg:
                error_msg = error_msg.replace(self.pixabay_api_key, '[API_KEY_HIDDEN]')
            self.logger.error(f'Error buscando en Pixabay: {error_msg}')
            return None
    
    def buscar_imagen_automatica(self, titulo: str, portal: str = '') -> Optional[Dict]:
        """Busca imagen usando sistema híbrido: Pexels -> Pixabay fallback"""
        keywords = self.generar_keywords_inteligentes(titulo, portal)
        
        # Intentar Pexels primero
        imagen = self.buscar_imagen_pexels(keywords)
        if imagen:
            self.logger.info(f'Imagen encontrada en Pexels para: {titulo[:50]}...')
            return imagen
        
        # Fallback a Pixabay
        imagen = self.buscar_imagen_pixabay(keywords)
        if imagen:
            self.logger.info(f'Imagen encontrada en Pixabay para: {titulo[:50]}...')
            return imagen
        
        self.logger.warning(f'No se encontró imagen para: {titulo[:50]}...')
        return None
    
    def optimizar_imagen(self, imagen_data: bytes, max_width: int = 1200, max_height: int = 800) -> bytes:
        """Optimiza imagen: resize y compresión"""
        try:
            # Abrir imagen con PIL
            imagen = Image.open(io.BytesIO(imagen_data))
            
            # Convertir a RGB si es necesario
            if imagen.mode in ('RGBA', 'LA', 'P'):
                imagen = imagen.convert('RGB')
            
            # Redimensionar manteniendo aspecto
            imagen.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Comprimir y guardar
            output = io.BytesIO()
            imagen.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            return output.getvalue()
            
        except Exception as e:
            self.logger.error(f'Error optimizando imagen: {str(e)}')
            return imagen_data  # Devolver original si falla
    
    def descargar_imagen(self, imagen_info: Dict, titulo: str) -> Optional[str]:
        """Descarga imagen y la guarda en media/noticias/imagenes/"""
        try:
            url = imagen_info['url']
            
            # Headers mejorados anti-bloqueo
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 EdgA/120.0.2210.144',
                'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'image',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'cross-site',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
            }
            
            # Intentar descarga con reintentos
            for intento in range(self.config.get('retry_attempts', 3)):
                try:
                    # Timeout específico: (conexión, lectura)
                    timeout_tuple = (
                        self.config.get('connection_timeout', 30),
                        self.config.get('read_timeout', 45)
                    )
                    
                    response = self.session.get(
                        url, 
                        headers=headers, 
                        timeout=timeout_tuple,
                        stream=True,
                        allow_redirects=True,
                        verify=True
                    )
                    response.raise_for_status()
                    break
                except Exception as e:
                    if intento == self.config.get('retry_attempts', 3) - 1:  # Último intento
                        raise e
                    time.sleep(1)  # Esperar antes del retry
            
            # Leer contenido
            imagen_data = b''
            total_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    total_size += len(chunk)
                    # Límite de seguridad: 10MB
                    if total_size > 10 * 1024 * 1024:
                        raise ValueError('Imagen excede límite de tamaño')
                    imagen_data += chunk
            
            # Validar que es imagen
            content_type = response.headers.get('content-type', '').lower()
            if not content_type.startswith('image/'):
                raise ValueError(f'Content-type no es imagen: {content_type}')
            
            # Optimizar imagen
            imagen_optimizada = self.optimizar_imagen(imagen_data)
            
            # Generar nombre único
            timestamp = int(time.time())
            titulo_limpio = ''.join(c for c in titulo.lower() if c.isalnum() or c.isspace()).replace(' ', '_')[:30]
            filename = f"{titulo_limpio}_{timestamp}_{imagen_info['source']}.jpg"
            
            # Guardar en media/noticias/imagenes/
            file_path = f'noticias/imagenes/{filename}'
            saved_path = default_storage.save(file_path, ContentFile(imagen_optimizada))
            
            self.logger.info(f'Imagen descargada y optimizada: {saved_path} ({total_size/1024:.1f}KB)')
            
            return saved_path
            
        except Exception as e:
            self.logger.error(f'Error descargando imagen: {str(e)}')
            return None
    
    def obtener_imagen_para_noticia(self, titulo: str, portal: str = '') -> Dict:
        """Método principal: busca, descarga y optimiza imagen para una noticia"""
        # Buscar imagen
        imagen_info = self.buscar_imagen_automatica(titulo, portal)
        
        if not imagen_info:
            return {
                'tipo': 'imagen',
                'imagen_url': '',
                'imagen_source': '',
                'imagen_alt': f'Imagen sobre {titulo[:50]}...'
            }
        
        # Descargar imagen
        imagen_path = self.descargar_imagen(imagen_info, titulo)
        
        if imagen_path:
            return {
                'tipo': 'imagen',
                'imagen_url': imagen_path,
                'imagen_source': imagen_info['source'],
                'imagen_original_url': imagen_info['url'],
                'imagen_author': imagen_info.get('photographer', 'Unknown'),
                'imagen_alt': imagen_info['alt'],
                'imagen_width': imagen_info.get('width'),
                'imagen_height': imagen_info.get('height')
            }
        else:
            return {
                'tipo': 'imagen',
                'imagen_url': '',
                'imagen_source': imagen_info['source'],
                'imagen_alt': imagen_info['alt']
            }


# Instancia global para reutilización
image_service = ImageService()