# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.blog.models import Noticia
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'EstefaniPUBLI - Limpiar noticias no deseadas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--inactivas',
            action='store_true',
            help='Eliminar solo noticias inactivas de Estefani'
        )
        parser.add_argument(
            '--todas-estefani',
            action='store_true',
            help='Eliminar TODAS las noticias de Estefani (activas e inactivas)'
        )
        parser.add_argument(
            '--antiguas',
            type=int,
            help='Eliminar noticias de Estefani más antiguas que X días'
        )
        parser.add_argument(
            '--por-ids',
            type=str,
            help='Eliminar noticias específicas por IDs (ej: 15,16,17 o 15-20)'
        )
        parser.add_argument(
            '--listar',
            action='store_true',
            help='Solo listar noticias sin eliminar'
        )
        parser.add_argument(
            '--confirmar',
            action='store_true',
            help='Confirmar antes de eliminar'
        )
        parser.add_argument(
            '--imagenes-huerfanas',
            action='store_true',
            help='Limpiar imágenes huérfanas sin noticia asociada'
        )

    def handle(self, *args, **options):
        inactivas = options['inactivas']
        todas_estefani = options['todas_estefani']
        antiguas = options['antiguas']
        por_ids = options['por_ids']
        listar = options['listar']
        confirmar = options['confirmar']
        imagenes_huerfanas = options['imagenes_huerfanas']
        
        self.stdout.write('EstefaniPUBLI - Limpieza de Noticias')
        self.stdout.write('='*50)
        
        # Manejar limpieza de imágenes huérfanas
        if imagenes_huerfanas:
            self.limpiar_imagenes_huerfanas()
            return
        
        # Determinar qué noticias eliminar
        noticias_a_eliminar = None
        descripcion = ""
        
        if todas_estefani:
            noticias_a_eliminar = Noticia.objects.filter(autor='Estefani')
            descripcion = "TODAS las noticias de Estefani"
        elif inactivas:
            noticias_a_eliminar = Noticia.objects.filter(autor='Estefani', activa=False)
            descripcion = "noticias INACTIVAS de Estefani"
        elif antiguas:
            fecha_limite = timezone.now() - timedelta(days=antiguas)
            noticias_a_eliminar = Noticia.objects.filter(
                autor='Estefani', 
                fecha_publicacion__lt=fecha_limite
            )
            descripcion = f"noticias de Estefani más antiguas que {antiguas} días"
        elif por_ids:
            ids_list = self.parse_ids(por_ids)
            noticias_a_eliminar = Noticia.objects.filter(
                id__in=ids_list,
                autor='Estefani'
            )
            descripcion = f"noticias de Estefani con IDs: {ids_list}"
        else:
            self.stdout.write(self.style.ERROR('ERROR: Debes especificar al menos un criterio de eliminación'))
            self.stdout.write('Opciones disponibles:')
            self.stdout.write('  --inactivas          : Solo noticias inactivas')
            self.stdout.write('  --todas-estefani     : TODAS las noticias de Estefani')
            self.stdout.write('  --antiguas=X         : Más antiguas que X días')
            self.stdout.write('  --por-ids=1,2,3      : Por IDs específicos')
            self.stdout.write('  --listar             : Solo mostrar sin eliminar')
            return
        
        # Mostrar noticias encontradas
        total_encontradas = noticias_a_eliminar.count()
        self.stdout.write(f'Encontradas {total_encontradas} {descripcion}')
        
        if total_encontradas == 0:
            self.stdout.write('No hay noticias que cumplan los criterios especificados')
            return
        
        self.stdout.write('\nNoticias encontradas:')
        for i, noticia in enumerate(noticias_a_eliminar.order_by('-id'), 1):
            estado = "ACTIVA" if noticia.activa else "INACTIVA"
            self.stdout.write(
                f'  {i}. ID:{noticia.id} | {estado} | {noticia.fecha_publicacion.strftime("%Y-%m-%d")} | {noticia.titulo[:60]}...'
            )
        
        if listar:
            self.stdout.write('\nModo listado - No se eliminara nada')
            return
        
        # Confirmar eliminación
        if confirmar or total_encontradas > 5:
            respuesta = input(f'\nELIMINAR {total_encontradas} noticias? (escriba "ELIMINAR" para confirmar): ')
            if respuesta != 'ELIMINAR':
                self.stdout.write('Operacion cancelada')
                return
        
        # Eliminar noticias
        self.stdout.write(f'\nEliminando {total_encontradas} noticias...')
        
        eliminadas = []
        for noticia in noticias_a_eliminar:
            eliminadas.append({
                'id': noticia.id,
                'titulo': noticia.titulo[:50],
                'fecha': noticia.fecha_publicacion.strftime("%Y-%m-%d")
            })
        
        # Realizar eliminación
        deleted_count = noticias_a_eliminar.delete()[0]
        
        # Mostrar resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write('RESUMEN DE LIMPIEZA')
        self.stdout.write('='*50)
        self.stdout.write(f'Noticias eliminadas: {deleted_count}')
        
        if deleted_count > 0:
            self.stdout.write('\nDetalle de noticias eliminadas:')
            for item in eliminadas:
                self.stdout.write(f'  - ID:{item["id"]} | {item["fecha"]} | {item["titulo"]}...')
            
            self.stdout.write(f'\nLimpieza completada exitosamente!')
        
        # Mostrar estado actual
        noticias_restantes = Noticia.objects.filter(autor='Estefani').count()
        self.stdout.write(f'\nNoticias de Estefani restantes: {noticias_restantes}')

    def parse_ids(self, ids_str):
        """Parsea string de IDs (ej: "15,16,17" o "15-20")"""
        ids = []
        partes = ids_str.split(',')
        
        for parte in partes:
            parte = parte.strip()
            if '-' in parte:
                # Rango (ej: "15-20")
                inicio, fin = map(int, parte.split('-'))
                ids.extend(range(inicio, fin + 1))
            else:
                # ID individual
                ids.append(int(parte))
        
        return ids
    
    def limpiar_imagenes_huerfanas(self):
        """Limpia imágenes huérfanas sin noticia asociada"""
        import os
        import glob
        from django.conf import settings
        
        self.stdout.write('Iniciando limpieza de imágenes huérfanas...')
        
        # Directorio de imágenes de noticias
        imagenes_dir = os.path.join(settings.MEDIA_ROOT, 'noticias', 'imagenes')
        
        if not os.path.exists(imagenes_dir):
            self.stdout.write('AVISO: Directorio de imágenes no existe')
            return
        
        # Obtener todas las imágenes en el directorio
        patron_imagenes = os.path.join(imagenes_dir, '*.*')
        archivos_imagenes = glob.glob(patron_imagenes)
        
        if not archivos_imagenes:
            self.stdout.write('INFO: No hay archivos de imagen para verificar')
            return
        
        self.stdout.write(f'Encontrados {len(archivos_imagenes)} archivos de imagen')
        
        # Obtener todas las noticias activas con imágenes
        noticias_con_imagenes = Noticia.objects.exclude(imagen='').exclude(imagen__isnull=True)
        imagenes_en_uso = set()
        
        for noticia in noticias_con_imagenes:
            if noticia.imagen:
                try:
                    imagenes_en_uso.add(noticia.imagen.path)
                except ValueError:
                    # Path inválido, ignorar
                    pass
        
        self.stdout.write(f'Encontradas {len(imagenes_en_uso)} imágenes vinculadas a noticias activas')
        
        # Identificar imágenes huérfanas
        imagenes_huerfanas = []
        for archivo in archivos_imagenes:
            if archivo not in imagenes_en_uso:
                imagenes_huerfanas.append(archivo)
        
        if not imagenes_huerfanas:
            self.stdout.write('INFO: No se encontraron imágenes huérfanas')
            return
        
        self.stdout.write(f'Encontradas {len(imagenes_huerfanas)} imágenes huérfanas:')
        
        # Mostrar lista de archivos huérfanos
        for i, archivo in enumerate(imagenes_huerfanas, 1):
            nombre_archivo = os.path.basename(archivo)
            tamaño = os.path.getsize(archivo) / 1024  # KB
            self.stdout.write(f'  {i}. {nombre_archivo} ({tamaño:.1f} KB)')
        
        # Calcular espacio total a liberar
        espacio_total = sum(os.path.getsize(archivo) for archivo in imagenes_huerfanas) / (1024 * 1024)  # MB
        self.stdout.write(f'Espacio total a liberar: {espacio_total:.2f} MB')
        
        # Confirmar eliminación
        respuesta = input('\n¿Eliminar estas imágenes huérfanas? (s/N): ').lower().strip()
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            self.stdout.write('Operación cancelada')
            return
        
        # Eliminar archivos
        eliminados = 0
        errores = 0
        
        for archivo in imagenes_huerfanas:
            try:
                os.remove(archivo)
                eliminados += 1
                self.stdout.write(f'Eliminado: {os.path.basename(archivo)}')
            except OSError as e:
                errores += 1
                self.stdout.write(f'Error eliminando {os.path.basename(archivo)}: {str(e)}')
        
        # Resumen final
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Limpieza completada:')
        self.stdout.write(f'   - Archivos eliminados: {eliminados}')
        self.stdout.write(f'   - Errores: {errores}')
        self.stdout.write(f'   - Espacio liberado: {espacio_total:.2f} MB')