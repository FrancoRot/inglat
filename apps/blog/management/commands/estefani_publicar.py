# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from apps.blog.models import Noticia, Categoria
import json
import os
import logging
import requests
from urllib.parse import urlparse
from datetime import datetime
import re


class Command(BaseCommand):
    help = 'EstefaniPUBLI - Publicar noticias desde JSON a Django Admin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--archivo',
            type=str,
            default='shared_memory/noticias_estefani.json',
            help='Archivo JSON con noticias a publicar (default: shared_memory/noticias_estefani.json)'
        )
        parser.add_argument(
            '--confirmar',
            action='store_true',
            help='Confirmar antes de cada publicación'
        )
        parser.add_argument(
            '--draft-mode',
            action='store_true',
            help='Crear noticias como inactivas (borrador)'
        )
        parser.add_argument(
            '--skip-images',
            action='store_true',
            help='Omitir descarga de imágenes'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular publicación sin crear registros'
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Modo debug con información detallada'
        )

    def handle(self, *args, **options):
        self.setup_logging(options['debug'])
        
        archivo_json = options['archivo']
        confirmar = options['confirmar']
        draft_mode = options['draft_mode']
        skip_images = options['skip_images']
        dry_run = options['dry_run']
        
        self.stdout.write('EstefaniPUBLI - Iniciando publicacion en Django Admin')
        
        # Verificar archivo JSON
        json_path = os.path.join(settings.BASE_DIR, archivo_json)
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'ERROR Archivo no encontrado: {json_path}'))
            self.stdout.write('INFO Ejecuta primero: python manage.py estefani_investigar')
            return
        
        # Cargar datos JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'ERROR cargando JSON: {str(e)}'))
            return
        
        noticias_data = session_data.get('noticias_procesadas', [])
        if not noticias_data:
            self.stdout.write(self.style.WARNING('WARN No hay noticias para publicar en el JSON'))
            return
        
        self.stdout.write(f'Archivo: {archivo_json}')
        self.stdout.write(f'Noticias a procesar: {len(noticias_data)}')
        self.stdout.write(f'Modo: {"BORRADOR" if draft_mode else "PUBLICADO"}')
        self.stdout.write(f'Imagenes: {"OMITIDAS" if skip_images else "PROCESADAS"}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('MODO SIMULACION - No se crearan registros'))
        
        # Verificar/crear categorías
        self.verificar_categorias()
        
        # Verificar que haya al menos una categoría activa
        categorias_activas = Categoria.objects.filter(activa=True).count()
        if categorias_activas == 0:
            self.stdout.write(self.style.ERROR('ERROR No hay categorias activas en la base de datos'))
            self.stdout.write('INFO Crea al menos una categoria en Django Admin antes de continuar')
            return
        
        self.stdout.write(f'OK Categorias activas disponibles: {categorias_activas}')
        
        # Procesar noticias
        publicaciones_exitosas = []
        publicaciones_fallidas = []
        
        for i, noticia_data in enumerate(noticias_data, 1):
            try:
                self.stdout.write(f'\nProcesando {i}/{len(noticias_data)}: {noticia_data["titulo"][:50]}...')
                
                if confirmar and not dry_run:
                    respuesta = input(f'Publicar esta noticia? (s/N): ')
                    if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
                        self.stdout.write('   SKIP Omitida por usuario')
                        continue
                
                # Verificar si ya existe
                if self.noticia_existe(noticia_data['titulo']):
                    self.stdout.write('   WARN Ya existe una noticia con titulo similar')
                    continue
                
                if dry_run:
                    self.stdout.write('   SIM SIMULACION: Se crearian los siguientes datos:')
                    self.mostrar_preview_noticia(noticia_data)
                    publicaciones_exitosas.append({
                        'titulo': noticia_data['titulo'],
                        'status': 'simulado',
                        'categoria': noticia_data.get('categoria_asignada', 'Sin categoría')
                    })
                else:
                    # Crear noticia real
                    noticia_creada = self.crear_noticia(
                        noticia_data, 
                        activa=not draft_mode,
                        skip_images=skip_images
                    )
                    
                    if noticia_creada:
                        publicaciones_exitosas.append({
                            'noticia_id': noticia_creada.id,
                            'titulo': noticia_creada.titulo,
                            'status': 'publicada' if not draft_mode else 'borrador',
                            'categoria': noticia_creada.categoria.nombre if noticia_creada.categoria else 'Sin categoría',
                            'url_admin': f'/admin/blog/noticia/{noticia_creada.id}/change/'
                        })
                        self.stdout.write(f'   OK Creada exitosamente (ID: {noticia_creada.id})')
                    else:
                        publicaciones_fallidas.append(noticia_data['titulo'])
                        self.stdout.write('   ERROR en la creacion')
                
            except Exception as e:
                self.logger.error(f'Error procesando noticia {noticia_data.get("titulo", "sin título")}: {str(e)}')
                self.stdout.write(f'   ERROR: {str(e)}')
                publicaciones_fallidas.append(noticia_data.get('titulo', 'Sin título'))
        
        # Mostrar resumen final
        self.mostrar_resumen_publicacion(publicaciones_exitosas, publicaciones_fallidas, dry_run)

    def setup_logging(self, debug=False):
        """Configura el sistema de logging"""
        log_dir = os.path.join(settings.BASE_DIR, 'shared_memory', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'estefani_publicacion.log')
        
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG if debug else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        self.logger = logging.getLogger(__name__)

    def verificar_categorias(self):
        """Verifica que existan todas las categorías necesarias"""
        categorias_requeridas = [
            {'nombre': 'Energía Solar', 'color': '#FFA500'},
            {'nombre': 'Tecnología', 'color': '#0066CC'},
            {'nombre': 'Noticias Sector', 'color': '#006466'},
            {'nombre': 'Sostenibilidad', 'color': '#228B22'},
            {'nombre': 'Instalaciones', 'color': '#8B4513'}
        ]
        
        for cat_data in categorias_requeridas:
            try:
                # Primero intentar obtener la categoría existente
                categoria = Categoria.objects.get(nombre=cat_data['nombre'])
                self.stdout.write(f'   OK Categoria existente: {categoria.nombre}')
            except Categoria.DoesNotExist:
                # Si no existe, crearla con manejo de errores
                try:
                    categoria = Categoria.objects.create(
                        nombre=cat_data['nombre'],
                        descripcion=f'Categoría para noticias de {cat_data["nombre"].lower()}',
                        color=cat_data['color'],
                        activa=True
                    )
                    self.stdout.write(f'   OK Categoria creada: {categoria.nombre}')
                except Exception as e:
                    # Si hay error de duplicado, intentar obtener de nuevo
                    try:
                        categoria = Categoria.objects.get(nombre=cat_data['nombre'])
                        self.stdout.write(f'   OK Categoria recuperada: {categoria.nombre}')
                    except Categoria.DoesNotExist:
                        self.stdout.write(f'   ERROR creando categoria {cat_data["nombre"]}: {str(e)}')
                        continue

    def noticia_existe(self, titulo):
        """Verifica si ya existe una noticia con título similar"""
        # Buscar títulos similares (primeras 50 caracteres)
        titulo_corto = titulo[:50].lower()
        exists = Noticia.objects.filter(titulo__icontains=titulo_corto).exists()
        return exists

    def mostrar_preview_noticia(self, noticia_data):
        """Muestra preview de la noticia en modo simulación"""
        self.stdout.write(f'      Título: {noticia_data["titulo"]}')
        self.stdout.write(f'      Categoría: {noticia_data.get("categoria_asignada", "Sin categoría")}')
        self.stdout.write(f'      Autor: {noticia_data.get("autor", "Estefani")}')
        self.stdout.write(f'      Contenido: {len(noticia_data.get("contenido", ""))} caracteres')
        self.stdout.write(f'      SEO: {noticia_data.get("seo", {}).get("meta_descripcion", "Sin meta descripción")[:50]}...')
        
        imagen_url = noticia_data.get('multimedia', {}).get('imagen_url', '')
        self.stdout.write(f'      Imagen: {"SÍ" if imagen_url else "NO"}')

    def crear_noticia(self, noticia_data, activa=True, skip_images=False):
        """Crea una nueva noticia respetando EXACTAMENTE la estructura del modelo Noticia"""
        try:
            # Obtener o crear categoría
            categoria = self.obtener_categoria(noticia_data.get('categoria_asignada'))
            
            # Preparar todos los campos del modelo Noticia
            titulo = noticia_data.get('titulo', '')[:200]  # Respetar max_length=200
            slug = ''  # Se genera automáticamente en el save()
            
            descripcion_corta = noticia_data.get('descripcion_corta', '')
            if len(descripcion_corta) > 300:  # Respetar max_length=300 del TextField
                descripcion_corta = descripcion_corta[:297] + '...'
            
            contenido = noticia_data.get('contenido', '')  # HTMLField sin límite
            autor = noticia_data.get('autor', 'Estefani')[:100]  # Respetar max_length
            
            # Campos de multimedia - respetando estructura exacta
            tipo_multimedia = 'imagen'  # Solo imagen por ahora
            imagen = None
            
            # Todos los campos de video (mantener vacíos para imágenes)
            video_url = ''
            video_platform = ''
            video_id = ''
            video_embed_url_cached = ''
            video_thumbnail_url = ''
            video_autoplay = False
            video_muted = True
            video_show_controls = True
            
            # Campos legacy de Vimeo (mantener vacíos)
            video_vimeo_url = ''
            video_vimeo_id = ''
            
            # SEO fields
            seo_data = noticia_data.get('seo', {})
            meta_descripcion = seo_data.get('meta_descripcion', '')[:160]  # max_length=160
            meta_keywords = seo_data.get('meta_keywords', '')[:200]  # max_length=200
            
            # Control fields
            destacada = False  # Por defecto no destacada
            orden = 0  # Orden por defecto
            
            # Fechas - se manejan automáticamente
            fecha_publicacion = timezone.now()
            
            # Crear instancia con TODOS los campos del modelo
            noticia = Noticia(
                # Campos principales
                titulo=titulo,
                slug=slug,  # Se autogenera
                descripcion_corta=descripcion_corta,
                contenido=contenido,
                
                # Multimedia
                tipo_multimedia=tipo_multimedia,
                imagen=imagen,  # Se asigna después si hay imagen
                video_url=video_url,
                video_platform=video_platform,
                video_id=video_id,
                video_embed_url_cached=video_embed_url_cached,
                video_thumbnail_url=video_thumbnail_url,
                video_autoplay=video_autoplay,
                video_muted=video_muted,
                video_show_controls=video_show_controls,
                
                # Campos legacy Vimeo
                video_vimeo_url=video_vimeo_url,
                video_vimeo_id=video_vimeo_id,
                
                # Metadatos
                autor=autor,
                categoria=categoria,
                fecha_publicacion=fecha_publicacion,
                
                # SEO
                meta_descripcion=meta_descripcion,
                meta_keywords=meta_keywords,
                
                # Control
                destacada=destacada,
                activa=activa,
                orden=orden
            )
            
            # Procesar imagen ANTES de guardar
            if not skip_images:
                imagen_url = noticia_data.get('multimedia', {}).get('imagen_url', '')
                if imagen_url and self.es_url_valida(imagen_url):
                    imagen_file = self.descargar_imagen(imagen_url, titulo)
                    if imagen_file:
                        noticia.imagen = imagen_file
            
            # Guardar noticia (ejecuta validaciones y save() del modelo)
            noticia.save()
            
            self.logger.info(f'Noticia creada: {noticia.titulo} (ID: {noticia.id})')
            self.stdout.write(f'      OK ID: {noticia.id}, Slug: {noticia.slug}')
            
            return noticia
            
        except Exception as e:
            self.logger.error(f'Error creando noticia: {str(e)}')
            self.stdout.write(f'      ERROR: {str(e)}')
            return None
    
    def obtener_categoria(self, categoria_nombre):
        """Obtiene la categoría especificada con fallback robusto"""
        if not categoria_nombre:
            # Usar la primera categoría activa como fallback
            categoria_fallback = Categoria.objects.filter(activa=True).first()
            if categoria_fallback:
                self.stdout.write(f'      INFO Usando categoria fallback: {categoria_fallback.nombre}')
            return categoria_fallback
        
        try:
            # Intentar obtener la categoría exacta
            categoria = Categoria.objects.get(nombre=categoria_nombre, activa=True)
            return categoria
        except Categoria.DoesNotExist:
            # Si no existe, buscar categorías similares
            try:
                # Buscar por nombre similar (ignorando mayúsculas)
                categoria = Categoria.objects.filter(
                    nombre__iexact=categoria_nombre, 
                    activa=True
                ).first()
                
                if categoria:
                    self.stdout.write(f'      OK Categoria encontrada (similar): {categoria.nombre}')
                    return categoria
                
                # Si no hay similar, usar la primera activa
                categoria_fallback = Categoria.objects.filter(activa=True).first()
                if categoria_fallback:
                    self.stdout.write(f'      WARN Categoria "{categoria_nombre}" no existe, usando: {categoria_fallback.nombre}')
                return categoria_fallback
                
            except Exception as e:
                self.logger.error(f'Error buscando categoría "{categoria_nombre}": {str(e)}')
                # Último recurso: primera categoría activa
                return Categoria.objects.filter(activa=True).first()

    def es_url_valida(self, url):
        """Verifica si una URL es válida"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def descargar_imagen(self, imagen_url, titulo):
        """Descarga una imagen desde URL y la convierte en Django File con validación robusta"""
        try:
            # Validar URL primero
            if not self.es_url_valida(imagen_url):
                self.logger.warning(f'URL inválida: {imagen_url}')
                return None
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Referer': imagen_url
            }
            
            self.stdout.write(f'      IMG Descargando imagen: {imagen_url[:60]}...')
            
            # Intentar descarga con timeout y retry
            for intento in range(3):
                try:
                    response = requests.get(
                        imagen_url, 
                        headers=headers, 
                        timeout=30, 
                        stream=True,
                        allow_redirects=True
                    )
                    response.raise_for_status()
                    break
                except requests.RequestException as e:
                    if intento == 2:  # Último intento
                        self.logger.warning(f'Error descargando imagen después de 3 intentos: {str(e)}')
                        return None
                    continue
            
            # Verificar content-type
            content_type = response.headers.get('content-type', '').lower()
            content_length = response.headers.get('content-length')
            
            # Validar que sea imagen
            if not content_type.startswith('image/'):
                self.logger.warning(f'Content-type no es imagen: {content_type} para {imagen_url}')
                return None
            
            # Verificar tamaño (evitar imágenes muy grandes o muy pequeñas)
            if content_length:
                size_mb = int(content_length) / (1024 * 1024)
                if size_mb > 10:  # Mayor a 10MB
                    self.logger.warning(f'Imagen demasiado grande: {size_mb:.1f}MB')
                    return None
                elif size_mb < 0.001:  # Menor a 1KB
                    self.logger.warning(f'Imagen demasiado pequeña: {size_mb:.1f}MB')
                    return None
            
            # Determinar extensión basada en content-type
            extension = '.jpg'  # default
            if 'png' in content_type:
                extension = '.png'
            elif 'gif' in content_type:
                extension = '.gif'
            elif 'webp' in content_type:
                extension = '.webp'
            elif 'jpeg' in content_type or 'jpg' in content_type:
                extension = '.jpg'
            elif 'svg' in content_type:
                extension = '.svg'
            
            # Descargar imagen a memoria
            image_data = b''
            total_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    total_size += len(chunk)
                    # Límite de seguridad: 10MB
                    if total_size > 10 * 1024 * 1024:
                        self.logger.warning(f'Imagen excede límite de tamaño: {imagen_url}')
                        return None
                    image_data += chunk
            
            # Verificar que tenemos datos válidos
            if len(image_data) < 1024:  # Menor a 1KB
                self.logger.warning(f'Imagen muy pequeña: {len(image_data)} bytes')
                return None
            
            # Crear archivo en memoria usando BytesIO
            from io import BytesIO
            image_buffer = BytesIO(image_data)
            
            # Crear nombre de archivo limpio
            titulo_limpio = re.sub(r'[^\w\-_\.]', '_', titulo[:30])
            filename = f"{titulo_limpio}_estefani{extension}"
            
            # Crear Django File
            django_file = File(image_buffer)
            django_file.name = filename
            
            self.stdout.write(f'      OK Imagen descargada: {filename} ({total_size/1024:.1f}KB)')
            return django_file
            
        except Exception as e:
            self.logger.error(f'Error descargando imagen {imagen_url}: {str(e)}')
            self.stdout.write(f'      ERROR descargando imagen: {str(e)[:50]}...')
            return None

    def mostrar_resumen_publicacion(self, exitosas, fallidas, dry_run):
        """Muestra resumen final de la publicación"""
        self.stdout.write('\n' + '='*60)
        modo = 'SIMULACIÓN' if dry_run else 'PUBLICACIÓN'
        self.stdout.write(f'RESUMEN ESTEFANI PUBLI - {modo} COMPLETADA')
        self.stdout.write('='*60)
        
        self.stdout.write(f'OK Exitosas: {len(exitosas)}')
        self.stdout.write(f'ERROR Fallidas: {len(fallidas)}')
        self.stdout.write(f'TOTAL procesadas: {len(exitosas) + len(fallidas)}')
        
        if exitosas:
            self.stdout.write('\nNoticias procesadas exitosamente:')
            for i, noticia in enumerate(exitosas, 1):
                status_icon = 'SIM' if dry_run else ('PUB' if noticia['status'] == 'publicada' else 'DRAFT')
                self.stdout.write(f'   {i}. {status_icon} {noticia["titulo"][:60]}... ({noticia["categoria"]})')
                if not dry_run and 'url_admin' in noticia:
                    self.stdout.write(f'      Admin: http://localhost:8000{noticia["url_admin"]}')
        
        if fallidas:
            self.stdout.write('\nNoticias con errores:')
            for i, titulo in enumerate(fallidas, 1):
                self.stdout.write(f'   {i}. {titulo}')
        
        if not dry_run and exitosas:
            self.stdout.write(f'\n{len(exitosas)} noticias procesadas exitosamente!')
            self.stdout.write('Accede al admin Django: http://localhost:8000/admin/blog/noticia/')
        elif dry_run:
            self.stdout.write(f'\nSimulacion completada. {len(exitosas)} noticias serian procesadas.')
            self.stdout.write('Para publicar realmente, ejecuta sin --dry-run')
        
        self.stdout.write(f'\nLog detallado: shared_memory/logs/estefani_publicacion.log')