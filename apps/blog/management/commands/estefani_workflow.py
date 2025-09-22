# -*- coding: utf-8 -*-
"""
Comando estefani_workflow - Flujo completo automatizado
Ejecuta: investigar + analizar + publicar en un solo comando
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
import logging
import os
from io import StringIO
import sys


class Command(BaseCommand):
    help = 'EstefaniPUBLI - Workflow completo: investigar + analizar + publicar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--max-noticias',
            type=int,
            default=5,
            help='Número máximo de noticias a procesar (default: 5)'
        )
        parser.add_argument(
            '--portales',
            type=str,
            default='todos',
            choices=['todos', 'argentina_only', 'regional'],
            help='Filtro de portales: todos, argentina_only, regional'
        )
        parser.add_argument(
            '--modo',
            type=str,
            default='completo',
            choices=['rapido', 'completo', 'exhaustivo'],
            help='Modo de investigación: rapido (3), completo (5), exhaustivo (8)'
        )
        parser.add_argument(
            '--analisis',
            type=str,
            choices=['impacto-ia', 'tendencias', 'competitividad', 'sostenibilidad'],
            default='impacto-ia',
            help='Tipo de análisis IA a agregar (default: impacto-ia)'
        )
        parser.add_argument(
            '--con-imagenes',
            action='store_true',
            help='Generar imágenes automáticamente usando APIs de Pexels/Pixabay'
        )
        parser.add_argument(
            '--auto-publicar',
            action='store_true',
            help='Publicar automáticamente las noticias al finalizar'
        )
        parser.add_argument(
            '--skip-analisis',
            action='store_true',
            help='Saltar paso de análisis IA (solo investigar + publicar)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular publicación sin crear registros reales'
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Modo debug con información detallada'
        )

    def handle(self, *args, **options):
        self.setup_logging(options['debug'])
        
        # Parámetros del workflow
        max_noticias = options['max_noticias']
        portales = options['portales']
        modo = options['modo']
        tipo_analisis = options['analisis']
        con_imagenes = options['con_imagenes']
        auto_publicar = options['auto_publicar']
        skip_analisis = options['skip_analisis']
        dry_run = options['dry_run']
        
        self.stdout.write('>> EstefaniPUBLI - WORKFLOW COMPLETO INICIADO')
        self.stdout.write('=' * 60)
        
        # Mostrar configuración del workflow
        config_info = [
            f'Max noticias: {max_noticias}',
            f'Portales: {portales}',
            f'Modo: {modo}',
            f'Imágenes: {"SÍ" if con_imagenes else "NO"}',
        ]
        
        if not skip_analisis:
            config_info.append(f'Análisis: {tipo_analisis}')
        else:
            config_info.append('Análisis: OMITIDO')
            
        if auto_publicar:
            config_info.append(f'Publicación: {"SIMULADA" if dry_run else "AUTOMÁTICA"}')
        else:
            config_info.append('Publicación: MANUAL')
            
        self.stdout.write('Configuración: ' + ' | '.join(config_info))
        self.stdout.write('=' * 60)
        
        # Archivos de trabajo
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        archivo_investigar = f'shared_memory/noticias_estefani_{timestamp}.json'
        archivo_analizar = f'shared_memory/noticias_estefani_{timestamp}_analizadas.json'
        
        try:
            # PASO 1: INVESTIGACIÓN
            self.stdout.write('\n>> PASO 1: INVESTIGACIÓN DE NOTICIAS')
            self.stdout.write('-' * 40)
            
            resultado_investigar = self.ejecutar_investigacion(
                max_noticias, portales, modo, con_imagenes, archivo_investigar
            )
            
            if not resultado_investigar:
                self.stdout.write(self.style.ERROR('ERROR: Falló la investigación de noticias'))
                return
                
            self.stdout.write('OK: Investigación completada exitosamente')
            
            # PASO 2: ANÁLISIS IA (opcional)
            archivo_final = archivo_investigar
            
            if not skip_analisis:
                self.stdout.write('\n>> PASO 2: ANÁLISIS IA')
                self.stdout.write('-' * 40)
                
                resultado_analisis = self.ejecutar_analisis(
                    archivo_investigar, tipo_analisis, archivo_analizar
                )
                
                if resultado_analisis:
                    archivo_final = archivo_analizar
                    self.stdout.write('OK: Análisis IA completado exitosamente')
                else:
                    self.stdout.write('WARN: Análisis falló, continuando con archivo original')
            else:
                self.stdout.write('\n>> PASO 2: ANÁLISIS IA - OMITIDO')
            
            # PASO 3: PUBLICACIÓN (opcional)
            if auto_publicar:
                self.stdout.write('\n>> PASO 3: PUBLICACIÓN')
                self.stdout.write('-' * 40)
                
                resultado_publicacion = self.ejecutar_publicacion(archivo_final, dry_run)
                
                if resultado_publicacion:
                    self.stdout.write('OK: Publicación completada exitosamente')
                else:
                    self.stdout.write('ERROR: Falló la publicación')
            else:
                self.stdout.write('\n>> PASO 3: PUBLICACIÓN - MANUAL')
                self.stdout.write('-' * 40)
                self.stdout.write(f'Para publicar ejecuta:')
                self.stdout.write(f'python manage.py estefani_publicar --archivo={archivo_final}')
            
            # RESUMEN FINAL
            self.mostrar_resumen_final(archivo_final, auto_publicar, dry_run)
            
        except Exception as e:
            self.logger.error(f'Error en workflow completo: {str(e)}')
            self.stdout.write(self.style.ERROR(f'❌ ERROR CRÍTICO: {str(e)}'))

    def setup_logging(self, debug):
        """Configura logging para el comando"""
        level = logging.DEBUG if debug else logging.INFO
        self.logger = logging.getLogger('estefani.workflow')
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.setLevel(level)

    def ejecutar_investigacion(self, max_noticias, portales, modo, con_imagenes, archivo_output):
        """Ejecuta el comando estefani_investigar"""
        try:
            # Preparar argumentos
            args = [
                f'--max-noticias={max_noticias}',
                f'--portales={portales}',
                f'--modo={modo}'
            ]
            
            if con_imagenes:
                args.append('--con-imagenes')
            
            # Ejecutar comando
            call_command('estefani_investigar', *args)
            
            # Verificar que se generó el archivo
            archivo_default = 'shared_memory/noticias_estefani.json'
            if os.path.exists(archivo_default):
                # Renombrar a archivo específico del workflow
                os.rename(archivo_default, archivo_output)
                return True
            else:
                self.logger.error('No se generó archivo de investigación')
                return False
                
        except Exception as e:
            self.logger.error(f'Error ejecutando investigación: {str(e)}')
            return False

    def ejecutar_analisis(self, archivo_input, tipo_analisis, archivo_output):
        """Ejecuta el comando estefani_analizar"""
        try:
            args = [
                f'--archivo={archivo_input}',
                f'--analisis={tipo_analisis}',
                f'--output={archivo_output}'
            ]
            
            call_command('estefani_analizar', *args)
            
            # Verificar que se generó el archivo
            return os.path.exists(archivo_output)
            
        except Exception as e:
            self.logger.error(f'Error ejecutando análisis: {str(e)}')
            return False

    def ejecutar_publicacion(self, archivo_input, dry_run):
        """Ejecuta el comando estefani_publicar"""
        try:
            args = [f'--archivo={archivo_input}']
            
            if dry_run:
                args.append('--dry-run')
            
            call_command('estefani_publicar', *args)
            return True
            
        except Exception as e:
            self.logger.error(f'Error ejecutando publicación: {str(e)}')
            return False

    def mostrar_resumen_final(self, archivo_final, auto_publicar, dry_run):
        """Muestra resumen final del workflow"""
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🎉 WORKFLOW ESTEFANI COMPLETADO')
        self.stdout.write('=' * 60)
        
        self.stdout.write(f'📁 Archivo final: {archivo_final}')
        
        if auto_publicar:
            if dry_run:
                self.stdout.write('📤 Estado: Simulación completada - NO se publicaron noticias')
                self.stdout.write('💡 Para publicar realmente ejecuta sin --dry-run')
            else:
                self.stdout.write('📤 Estado: Noticias publicadas en Django Admin')
                self.stdout.write('🔗 Ver en: http://localhost:8000/admin/blog/noticia/')
        else:
            self.stdout.write('📤 Estado: Listo para publicación manual')
            self.stdout.write(f'💡 Ejecuta: python manage.py estefani_publicar --archivo={archivo_final}')
        
        # Información adicional
        if os.path.exists(archivo_final):
            try:
                import json
                with open(archivo_final, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_noticias = len(data.get('noticias_procesadas', []))
                    self.stdout.write(f'📊 Total noticias: {total_noticias}')
                    
                    # Mostrar títulos
                    if total_noticias > 0:
                        self.stdout.write('\n📰 Noticias generadas:')
                        for i, noticia in enumerate(data['noticias_procesadas'], 1):
                            titulo = noticia.get('titulo', 'Sin título')[:60]
                            tiene_imagen = 'SÍ' if noticia.get('multimedia', {}).get('imagen_url') else 'NO'
                            tiene_analisis = 'SÍ' if 'analisis_agregado' in noticia else 'NO'
                            self.stdout.write(f'   {i}. {titulo}... (IMG: {tiene_imagen}, IA: {tiene_analisis})')
            except:
                pass
        
        self.stdout.write('\n✨ ¡Proceso completado exitosamente!')
        self.stdout.write('=' * 60)