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


class Command(BaseCommand):
    help = 'EstefaniPUBLI - Publicar noticias específicas desde JSON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--archivo',
            type=str,
            default='shared_memory/noticias_estefani.json',
            help='Archivo JSON con noticias (default: shared_memory/noticias_estefani.json)'
        )
        parser.add_argument(
            '--indices',
            type=str,
            help='Índices de noticias a publicar (ej: 1,3,5 o 1-3)'
        )
        parser.add_argument(
            '--titulo-contiene',
            type=str,
            help='Publicar solo noticias que contengan este texto en el título'
        )
        parser.add_argument(
            '--categoria',
            type=str,
            help='Publicar solo noticias de esta categoría'
        )
        parser.add_argument(
            '--listar',
            action='store_true',
            help='Solo listar noticias disponibles sin publicar'
        )
        parser.add_argument(
            '--draft-mode',
            action='store_true',
            help='Crear como borradores (inactivas)'
        )
        parser.add_argument(
            '--skip-images',
            action='store_true',
            help='Omitir descarga de imágenes'
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Modo debug'
        )

    def handle(self, *args, **options):
        self.setup_logging(options['debug'])
        
        archivo_json = options['archivo']
        indices = options['indices']
        titulo_contiene = options['titulo_contiene']
        categoria = options['categoria']
        listar = options['listar']
        draft_mode = options['draft_mode']
        skip_images = options['skip_images']
        
        self.stdout.write('EstefaniPUBLI - Publicación Selectiva')
        
        # Cargar JSON
        json_path = os.path.join(settings.BASE_DIR, archivo_json)
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'ERROR Archivo no encontrado: {json_path}'))
            return
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'ERROR cargando JSON: {str(e)}'))
            return
        
        noticias_data = session_data.get('noticias_procesadas', [])
        if not noticias_data:
            self.stdout.write(self.style.WARNING('WARN No hay noticias en el JSON'))
            return
        
        # Mostrar todas las noticias disponibles
        self.stdout.write(f'\nNoticias disponibles ({len(noticias_data)}):')
        for i, noticia in enumerate(noticias_data, 1):
            categoria_nombre = noticia.get('categoria_asignada', 'Sin categoría')
            self.stdout.write(f'   {i}. {noticia["titulo"][:60]}... ({categoria_nombre})')
        
        # Filtrar noticias según criterios
        noticias_filtradas = self.filtrar_noticias(
            noticias_data, indices, titulo_contiene, categoria
        )
        
        if not noticias_filtradas:
            self.stdout.write(self.style.WARNING('WARN No se encontraron noticias con los criterios especificados'))
            return
        
        self.stdout.write(f'\nNoticias seleccionadas ({len(noticias_filtradas)}):')
        for i, noticia in enumerate(noticias_filtradas, 1):
            categoria_nombre = noticia.get('categoria_asignada', 'Sin categoría')
            self.stdout.write(f'   {i}. {noticia["titulo"][:60]}... ({categoria_nombre})')
        
        if listar:
            self.stdout.write('\nModo listado - No se publicaran noticias')
            return
        
        # Confirmar publicación
        respuesta = input(f'\nPublicar {len(noticias_filtradas)} noticias? (s/N): ')
        if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
            self.stdout.write('ERROR Publicacion cancelada')
            return
        
        # Verificar categorías
        self.verificar_categorias()
        
        # Publicar noticias filtradas
        publicaciones_exitosas = []
        publicaciones_fallidas = []
        
        for i, noticia_data in enumerate(noticias_filtradas, 1):
            try:
                self.stdout.write(f'\nPublicando {i}/{len(noticias_filtradas)}: {noticia_data["titulo"][:50]}...')
                
                # Verificar si ya existe
                if self.noticia_existe(noticia_data['titulo']):
                    self.stdout.write('   WARN Ya existe una noticia con titulo similar')
                    continue
                
                # Crear noticia
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
                self.logger.error(f'Error procesando noticia: {str(e)}')
                self.stdout.write(f'   ERROR: {str(e)}')
                publicaciones_fallidas.append(noticia_data.get('titulo', 'Sin título'))
        
        # Mostrar resumen
        self.mostrar_resumen_publicacion(publicaciones_exitosas, publicaciones_fallidas, False)

    def filtrar_noticias(self, noticias_data, indices, titulo_contiene, categoria):
        """Filtra noticias según criterios especificados"""
        noticias_filtradas = []
        
        for i, noticia in enumerate(noticias_data, 1):
            incluir = True
            
            # Filtrar por índices
            if indices:
                indices_list = self.parse_indices(indices)
                if i not in indices_list:
                    incluir = False
            
            # Filtrar por título
            if titulo_contiene and titulo_contiene.lower() not in noticia['titulo'].lower():
                incluir = False
            
            # Filtrar por categoría
            if categoria and categoria.lower() not in noticia.get('categoria_asignada', '').lower():
                incluir = False
            
            if incluir:
                noticias_filtradas.append(noticia)
        
        return noticias_filtradas

    def parse_indices(self, indices_str):
        """Parsea string de índices (ej: "1,3,5" o "1-3")"""
        indices = []
        partes = indices_str.split(',')
        
        for parte in partes:
            parte = parte.strip()
            if '-' in parte:
                # Rango (ej: "1-3")
                inicio, fin = map(int, parte.split('-'))
                indices.extend(range(inicio, fin + 1))
            else:
                # Índice individual
                indices.append(int(parte))
        
        return indices

    def setup_logging(self, debug=False):
        """Configura el sistema de logging"""
        log_dir = os.path.join(settings.BASE_DIR, 'shared_memory', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'estefani_publicacion_selectiva.log')
        
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG if debug else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        self.logger = logging.getLogger(__name__)

    def verificar_categorias(self):
        """Verifica que existan las categorías necesarias"""
        categorias_requeridas = [
            {'nombre': 'Energía Solar', 'color': '#FFA500'},
            {'nombre': 'Tecnología', 'color': '#0066CC'},
            {'nombre': 'Noticias Sector', 'color': '#006466'},
            {'nombre': 'Sostenibilidad', 'color': '#228B22'},
            {'nombre': 'Instalaciones', 'color': '#8B4513'}
        ]
        
        for cat_data in categorias_requeridas:
            try:
                categoria = Categoria.objects.get(nombre=cat_data['nombre'])
            except Categoria.DoesNotExist:
                try:
                    categoria = Categoria.objects.create(
                        nombre=cat_data['nombre'],
                        descripcion=f'Categoría para noticias de {cat_data["nombre"].lower()}',
                        color=cat_data['color'],
                        activa=True
                    )
                except Exception:
                    pass

    def noticia_existe(self, titulo):
        """Verifica si ya existe una noticia con título similar"""
        titulo_corto = titulo[:50].lower()
        return Noticia.objects.filter(titulo__icontains=titulo_corto).exists()

    def crear_noticia(self, noticia_data, activa=True, skip_images=False):
        """Crea una nueva noticia"""
        try:
            # Obtener categoría
            categoria = self.obtener_categoria(noticia_data.get('categoria_asignada'))
            
            # Preparar campos
            titulo = noticia_data.get('titulo', '')[:200]
            descripcion_corta = noticia_data.get('descripcion_corta', '')[:300]
            contenido = noticia_data.get('contenido', '')
            autor = noticia_data.get('autor', 'Estefani')[:100]
            
            # SEO fields
            seo_data = noticia_data.get('seo', {})
            meta_descripcion = seo_data.get('meta_descripcion', '')[:160]
            meta_keywords = seo_data.get('meta_keywords', '')[:200]
            
            # Crear noticia
            noticia = Noticia(
                titulo=titulo,
                descripcion_corta=descripcion_corta,
                contenido=contenido,
                autor=autor,
                categoria=categoria,
                meta_descripcion=meta_descripcion,
                meta_keywords=meta_keywords,
                activa=activa,
                destacada=False,
                orden=0
            )
            
            # Procesar imagen
            if not skip_images:
                imagen_url = noticia_data.get('multimedia', {}).get('imagen_url', '')
                if imagen_url and self.es_url_valida(imagen_url):
                    imagen_file = self.descargar_imagen(imagen_url, titulo)
                    if imagen_file:
                        noticia.imagen = imagen_file
            
            noticia.save()
            return noticia
            
        except Exception as e:
            self.logger.error(f'Error creando noticia: {str(e)}')
            return None

    def obtener_categoria(self, categoria_nombre):
        """Obtiene la categoría especificada"""
        if not categoria_nombre:
            return Categoria.objects.filter(activa=True).first()
        
        try:
            return Categoria.objects.get(nombre=categoria_nombre, activa=True)
        except Categoria.DoesNotExist:
            return Categoria.objects.filter(activa=True).first()

    def es_url_valida(self, url):
        """Verifica si una URL es válida"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def descargar_imagen(self, imagen_url, titulo):
        """Descarga una imagen desde URL"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(imagen_url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                self.logger.warning(f'Tipo de contenido no es imagen: {content_type}')
                return None
            
            # Detectar extensión
            extension = '.jpg'
            if 'png' in content_type.lower():
                extension = '.png'
            elif 'gif' in content_type.lower():
                extension = '.gif'
            elif 'webp' in content_type.lower():
                extension = '.webp'
            elif 'jpeg' in content_type.lower():
                extension = '.jpg'
            
            # Descargar imagen a memoria
            image_data = b''
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    image_data += chunk
            
            # Validar que tenemos datos
            if len(image_data) < 100:  # Muy pequeña para ser imagen válida
                self.logger.warning(f'Imagen muy pequeña: {len(image_data)} bytes')
                return None
            
            # Crear archivo temporal con los datos
            from io import BytesIO
            image_buffer = BytesIO(image_data)
            
            # Crear nombre de archivo limpio
            titulo_limpio = titulo[:30].replace(' ', '_').replace('/', '_').replace('\\', '_')
            filename = f"{titulo_limpio}_estefani{extension}"
            
            # Crear Django File
            django_file = File(image_buffer)
            django_file.name = filename
            
            self.logger.info(f'Imagen descargada exitosamente: {len(image_data)} bytes, tipo: {content_type}')
            return django_file
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Error de red descargando imagen: {str(e)}')
            return None
        except Exception as e:
            self.logger.error(f'Error general descargando imagen: {str(e)}')
            return None

    def mostrar_resumen_publicacion(self, exitosas, fallidas, dry_run):
        """Muestra resumen final"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write('RESUMEN PUBLICACION SELECTIVA')
        self.stdout.write('='*60)
        
        self.stdout.write(f'OK Exitosas: {len(exitosas)}')
        self.stdout.write(f'ERROR Fallidas: {len(fallidas)}')
        
        if exitosas:
            self.stdout.write('\nNoticias publicadas:')
            for i, noticia in enumerate(exitosas, 1):
                status_icon = 'PUB' if noticia['status'] == 'publicada' else 'DRAFT'
                self.stdout.write(f'   {i}. {status_icon} {noticia["titulo"][:60]}... ({noticia["categoria"]})')
                self.stdout.write(f'      Admin: http://localhost:8000{noticia["url_admin"]}')
        
        if fallidas:
            self.stdout.write('\nNoticias con errores:')
            for i, titulo in enumerate(fallidas, 1):
                self.stdout.write(f'   {i}. {titulo}')
        
        if exitosas:
            self.stdout.write(f'\n{len(exitosas)} noticias publicadas exitosamente!')
            self.stdout.write('Admin Django: http://localhost:8000/admin/blog/noticia/')

