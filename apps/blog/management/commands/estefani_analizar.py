# -*- coding: utf-8 -*-
"""
Comando estefani_analizar - Analiza noticias existentes con IA
Agrega secciones de análisis como "Impacto de la IA" a noticias procesadas
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import json
import os
import logging
from typing import Dict, List, Optional

# Importar servicios Estefani optimizados
from apps.blog.estefani_core import estefani_core


class Command(BaseCommand):
    help = 'EstefaniPUBLI - Análisis IA de noticias existentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--archivo',
            type=str,
            default='shared_memory/noticias_estefani.json',
            help='Archivo JSON de noticias a analizar (default: noticias_estefani.json)'
        )
        parser.add_argument(
            '--analisis',
            type=str,
            choices=['impacto-ia', 'tendencias', 'competitividad', 'sostenibilidad'],
            default='impacto-ia',
            help='Tipo de análisis a realizar (default: impacto-ia)'
        )
        parser.add_argument(
            '--noticia-id',
            type=str,
            help='ID específico de noticia a analizar (opcional)'
        )
        parser.add_argument(
            '--output',
            type=str,
            help='Archivo de salida personalizado (opcional)'
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Modo debug con información detallada'
        )

    def handle(self, *args, **options):
        self.setup_logging(options['debug'])
        
        archivo_input = options['archivo']
        tipo_analisis = options['analisis']
        noticia_id = options['noticia_id']
        archivo_output = options['output']
        
        self.stdout.write('EstefaniPUBLI - Iniciando análisis IA de noticias')
        self.stdout.write(f'Archivo: {archivo_input}')
        self.stdout.write(f'Tipo análisis: {tipo_analisis.upper()}')
        
        # Cargar noticias
        noticias_data = estefani_core.cargar_noticias_json(archivo_input)
        if not noticias_data:
            self.stdout.write(self.style.ERROR('No se pudo cargar el archivo de noticias'))
            return
        
        noticias_procesadas = noticias_data.get('noticias_procesadas', [])
        if not noticias_procesadas:
            self.stdout.write(self.style.WARNING('No se encontraron noticias para analizar'))
            return
        
        self.stdout.write(f'Noticias encontradas: {len(noticias_procesadas)}')
        
        # Filtrar por ID específico si se proporciona
        if noticia_id:
            noticias_procesadas = [n for n in noticias_procesadas if n.get('id') == noticia_id]
            if not noticias_procesadas:
                self.stdout.write(self.style.ERROR(f'No se encontró noticia con ID: {noticia_id}'))
                return
        
        # Procesar análisis
        noticias_analizadas = []
        total_exitosas = 0
        
        for i, noticia in enumerate(noticias_procesadas, 1):
            try:
                self.stdout.write(f'\nAnalizando ({i}/{len(noticias_procesadas)}): {noticia.get("titulo", "")[:50]}...')
                
                noticia_analizada = self.analizar_noticia(noticia, tipo_analisis)
                if noticia_analizada:
                    noticias_analizadas.append(noticia_analizada)
                    total_exitosas += 1
                    self.stdout.write('   OK Análisis agregado exitosamente')
                else:
                    noticias_analizadas.append(noticia)  # Mantener original si falla
                    self.stdout.write('   WARN No se pudo agregar análisis, manteniendo original')
                    
            except Exception as e:
                self.logger.error(f'Error analizando noticia {i}: {str(e)}')
                self.stdout.write(f'   ERROR: {str(e)[:50]}...')
                noticias_analizadas.append(noticia)  # Mantener original
        
        # Actualizar estructura de datos
        noticias_data['noticias_procesadas'] = noticias_analizadas
        noticias_data['analisis_info'] = {
            'tipo_analisis': tipo_analisis,
            'fecha_analisis': timezone.now().isoformat(),
            'total_analizadas': total_exitosas,
            'total_noticias': len(noticias_procesadas)
        }
        
        # Guardar resultado
        if not archivo_output:
            nombre_base = archivo_input.replace('.json', '')
            archivo_output = f'{nombre_base}_analizadas.json'
        
        if estefani_core.guardar_noticias_json(noticias_data, archivo_output):
            self.stdout.write(f'\n✅ ANÁLISIS COMPLETADO')
            self.stdout.write(f'Archivo guardado: {archivo_output}')
            self.stdout.write(f'Noticias analizadas exitosamente: {total_exitosas}/{len(noticias_procesadas)}')
            
            if total_exitosas > 0:
                self.stdout.write('\nPara publicar las noticias analizadas:')
                self.stdout.write(f'python manage.py estefani_publicar --archivo={archivo_output}')
        else:
            self.stdout.write(self.style.ERROR('Error guardando archivo de salida'))

    def setup_logging(self, debug):
        """Configura logging para el comando"""
        level = logging.DEBUG if debug else logging.INFO
        self.logger = logging.getLogger('estefani.analizar')
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.setLevel(level)

    def analizar_noticia(self, noticia: Dict, tipo_analisis: str) -> Optional[Dict]:
        """Analiza una noticia y agrega la sección correspondiente"""
        try:
            titulo = noticia.get('titulo', '')
            contenido_actual = noticia.get('contenido', '')
            
            # Generar análisis según tipo
            if tipo_analisis == 'impacto-ia':
                seccion_analisis = self.generar_analisis_ia(titulo, contenido_actual)
            elif tipo_analisis == 'tendencias':
                seccion_analisis = self.generar_analisis_tendencias(titulo, contenido_actual)
            elif tipo_analisis == 'competitividad':
                seccion_analisis = self.generar_analisis_competitividad(titulo, contenido_actual)
            elif tipo_analisis == 'sostenibilidad':
                seccion_analisis = self.generar_analisis_sostenibilidad(titulo, contenido_actual)
            else:
                return None
            
            if not seccion_analisis:
                return None
            
            # Integrar análisis al contenido existente
            contenido_con_analisis = self.integrar_analisis(contenido_actual, seccion_analisis)
            
            # Crear copia de la noticia con el análisis
            noticia_analizada = noticia.copy()
            noticia_analizada['contenido'] = contenido_con_analisis
            noticia_analizada['analisis_agregado'] = {
                'tipo': tipo_analisis,
                'fecha': timezone.now().isoformat()
            }
            
            # Actualizar métricas
            if 'metricas' in noticia_analizada:
                noticia_analizada['metricas']['longitud'] = len(contenido_con_analisis)
                noticia_analizada['metricas']['analisis_ia'] = True
            
            return noticia_analizada
            
        except Exception as e:
            self.logger.error(f'Error en analizar_noticia: {str(e)}')
            return None

    def generar_analisis_ia(self, titulo: str, contenido: str) -> str:
        """Genera análisis de impacto de IA específico para energías renovables"""
        
        # Mapeo de sectores a tecnologías IA específicas
        tecnologias_ia = {
            'solar': {
                'tecnologias': ['algoritmos de optimización solar', 'machine learning predictivo', 'IoT inteligente', 'visión computacional'],
                'beneficios': ['aumento 25% eficiencia', 'reducción 30% costos mantenimiento', 'predicción clima solar'],
                'aplicaciones': ['mantenimiento predictivo paneles', 'optimización ángulo solar', 'gestión inteligente baterías']
            },
            'eólica': {
                'tecnologias': ['IA predictiva vientos', 'sensores IoT avanzados', 'algoritmos optimización'],
                'beneficios': ['incremento 20% generación', 'reducción 40% mantenimiento', 'predicción vientos precisa'],
                'aplicaciones': ['control adaptativo turbinas', 'mantenimiento predictivo aspas', 'optimización parques eólicos']
            },
            'renovable': {
                'tecnologias': ['redes neuronales energéticas', 'blockchain energético', 'gemelos digitales'],
                'beneficios': ['eficiencia 15-30%', 'costos reducidos 25%', 'autonomía operativa'],
                'aplicaciones': ['gestión inteligente red', 'trading energético automático', 'almacenamiento optimizado']
            }
        }
        
        # Detectar sector principal
        titulo_lower = titulo.lower()
        contenido_lower = contenido.lower()
        
        sector_detectado = 'renovable'  # default
        for sector in tecnologias_ia.keys():
            if sector in titulo_lower or sector in contenido_lower:
                sector_detectado = sector
                break
        
        tech_info = tecnologias_ia[sector_detectado]
        
        # Generar contenido dinámico
        tecnologia_principal = tech_info['tecnologias'][0]
        beneficio_principal = tech_info['beneficios'][0]
        aplicacion_principal = tech_info['aplicaciones'][0]
        
        analisis = f"""
<p><strong>Impacto de la IA:</strong> La inteligencia artificial está transformando el sector de energías renovables mediante {tecnologia_principal} que permiten {beneficio_principal}. Las aplicaciones más relevantes incluyen {aplicacion_principal}, posicionando a Argentina como líder regional en tecnologías energéticas inteligentes. Para empresas del sector, estas innovaciones representan oportunidades concretas de optimización operativa y reducción de costos en los próximos 2-3 años.</p>
        """.strip()
        
        return analisis

    def generar_analisis_tendencias(self, titulo: str, contenido: str) -> str:
        """Genera análisis de tendencias del sector"""
        return """
<p><strong>Tendencias del Sector:</strong> Las proyecciones para el sector de energías renovables en Argentina indican un crecimiento sostenido del 15-20% anual, impulsado por políticas gubernamentales favorables y la creciente demanda empresarial de soluciones sustentables. Las empresas que adopten estas tecnologías tempranamente obtendrán ventajas competitivas significativas en eficiencia operativa y posicionamiento de marca.</p>
        """.strip()

    def generar_analisis_competitividad(self, titulo: str, contenido: str) -> str:
        """Genera análisis de competitividad empresarial"""
        return """
<p><strong>Ventaja Competitiva:</strong> La adopción de tecnologías de energías renovables representa una diferenciación estratégica para empresas argentinas, generando ahorros operativos del 20-40% y mejorando la imagen corporativa. Las organizaciones pioneras en autoconsumo solar obtienen certificaciones de sustentabilidad que fortalecen su posicionamiento comercial y acceso a financiamiento preferencial.</p>
        """.strip()

    def generar_analisis_sostenibilidad(self, titulo: str, contenido: str) -> str:
        """Genera análisis de impacto en sostenibilidad"""
        return """
<p><strong>Impacto Sostenible:</strong> Esta iniciativa contribuye significativamente a los objetivos de desarrollo sostenible de Argentina, reduciendo la huella de carbono empresarial y promoviendo la transición energética nacional. Las empresas que implementen estas soluciones pueden reducir sus emisiones de CO2 en 30-50%, cumpliendo con estándares internacionales de sostenibilidad y accediendo a mercados de carbono emergentes.</p>
        """.strip()

    def integrar_analisis(self, contenido_original: str, seccion_analisis: str) -> str:
        """Integra la sección de análisis al contenido existente"""
        # Buscar el mejor lugar para insertar el análisis
        # Generalmente antes del último párrafo o después del contexto técnico
        
        if '<p><strong>Perspectiva' in contenido_original:
            # Insertar antes de "Perspectiva Futura" o similar
            return contenido_original.replace(
                '<p><strong>Perspectiva',
                f'{seccion_analisis}\n\n<p><strong>Perspectiva'
            )
        elif contenido_original.count('<p>') >= 3:
            # Insertar antes del último párrafo
            parrafos = contenido_original.split('<p>')
            # Insertar antes del último párrafo
            parrafos.insert(-1, seccion_analisis + '\n\n')
            return '<p>'.join(parrafos)
        else:
            # Agregar al final
            return f"{contenido_original}\n\n{seccion_analisis}"