# -*- coding: utf-8 -*-
"""
EstefaniCore - Funciones compartidas para optimización de tokens y código
Evita duplicación entre comandos estefani_investigar, estefani_analizar, etc.
"""
import logging
import json
import time
from typing import Dict, List, Optional
from django.utils import timezone
from django.conf import settings


class EstefaniCore:
    """Clase base con funciones compartidas para todos los comandos Estefani"""
    
    def __init__(self):
        self.logger = logging.getLogger('estefani.core')
    
    # PLANTILLAS OPTIMIZADAS (reutilizables entre comandos)
    
    def get_plantilla_profesional(self, titulo: str, descripcion: str, portal: str) -> str:
        """Plantilla profesional optimizada para tokens"""
        return f"""
Genera una noticia profesional basada en: "{titulo}"
Fuente: {portal} | Descripción: {descripcion}

ESTRUCTURA REQUERIDA (HTML limpio):
<p><strong>Introducción:</strong> [contextualización argentina del tema]</p>
<p>[desarrollo del impacto para mercado de autoconsumo empresarial argentino]</p>
<p><strong>Contexto:</strong> [implicaciones técnicas y comerciales]</p>
<p>[perspectiva INGLAT para empresas argentinas]</p>
<p><strong>Impacto:</strong> [relevancia para RenovAr y generación distribuida]</p>

REQUISITOS:
- 600-800 palabras
- Enfoque empresarial argentino
- Reformulación 100% original
- HTML simple (p, strong, blockquote únicamente)
- Integrar perspectiva INGLAT como líder en autoconsumo solar
        """.strip()
    
    def get_plantilla_empresarial(self, titulo: str, descripcion: str, portal: str) -> str:
        """Plantilla empresarial optimizada"""
        return f"""
Crea análisis empresarial de: "{titulo}"
Fuente: {portal} | Base: {descripcion}

FORMATO:
<p><strong>Contexto empresarial:</strong> [impacto sector empresarial argentino]</p>
<p>[oportunidades concretas autoconsumo solar]</p>
<p><strong>Beneficios:</strong></p>
<ul><li>[beneficio 1 específico]</li><li>[beneficio 2 medible]</li><li>[beneficio 3 competitivo]</li></ul>
<p><strong>Perspectiva INGLAT:</strong> [posicionamiento como expertos]</p>

ENFOQUE: Empresas argentinas, ROI, competitividad, sostenibilidad
LONGITUD: 500-700 palabras
        """.strip()
    
    def get_plantilla_analisis_ia(self, titulo: str, contenido: str) -> str:
        """Plantilla para análisis de impacto IA - NUEVO"""
        return f"""
Agrega una sección "Impacto de la IA" al siguiente contenido sobre: "{titulo}"

CONTENIDO BASE:
{contenido[:500]}...

GENERA SOLO la sección nueva:
<p><strong>Impacto de la IA:</strong> [Análisis específico de cómo la inteligencia artificial está transformando o transformará este sector energético. Incluir tecnologías específicas (machine learning, IoT, algoritmos predictivos), beneficios cuantificables (% de eficiencia, reducción costos), y proyección temporal (2-5 años). Enfoque en aplicaciones empresariales argentinas.]</p>

REQUISITOS:
- Tecnologías IA específicas para energía renovable
- Beneficios medibles y concretos
- Contexto empresarial argentino
- 100-150 palabras máximo
- HTML simple únicamente
        """.strip()
    
    # FUNCIONES UTILITARIAS COMPARTIDAS
    
    def generar_session_id(self, prefix: str = "estefani") -> str:
        """Genera ID único para sesiones"""
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        return f"{prefix}_{timestamp}"
    
    def limpiar_titulo(self, titulo: str, max_length: int = 200) -> str:
        """Limpia y valida títulos"""
        if not titulo:
            return ""
        
        # Limpiar caracteres extraños
        titulo = titulo.strip()
        titulo = ' '.join(titulo.split())  # Normalizar espacios
        
        # Truncar si es necesario
        if len(titulo) > max_length:
            titulo = titulo[:max_length-3] + "..."
        
        return titulo
    
    def extraer_keywords_principales(self, titulo: str) -> List[str]:
        """Extrae keywords principales de un título para SEO"""
        # Keywords principales del sector
        keywords_base = [
            'energía solar', 'solar', 'fotovoltaica', 'autoconsumo', 
            'paneles solares', 'renovable', 'energía limpia', 'sostenible',
            'eficiencia energética', 'generación distribuida', 'argentina',
            'empresarial', 'instalación', 'ahorro energético'
        ]
        
        titulo_lower = titulo.lower()
        keywords_encontradas = []
        
        for keyword in keywords_base:
            if keyword in titulo_lower:
                keywords_encontradas.append(keyword)
        
        # Agregar términos específicos del título
        palabras_titulo = [word for word in titulo_lower.split() if len(word) > 4]
        keywords_encontradas.extend(palabras_titulo[:3])
        
        return list(set(keywords_encontradas))[:8]  # Max 8 keywords
    
    def generar_meta_seo(self, titulo: str, descripcion: str) -> Dict[str, str]:
        """Genera metadatos SEO optimizados"""
        # Meta título (max 60 chars)
        meta_titulo = titulo[:57] + "..." if len(titulo) > 60 else titulo
        meta_titulo += " | INGLAT"
        
        # Meta descripción (max 160 chars) 
        if len(descripcion) > 155:
            meta_descripcion = descripcion[:152] + "..."
        else:
            meta_descripcion = descripcion
        
        # Keywords
        keywords = self.extraer_keywords_principales(titulo)
        meta_keywords = ", ".join(keywords)
        
        return {
            'meta_titulo': meta_titulo,
            'meta_descripcion': meta_descripcion,
            'meta_keywords': meta_keywords
        }
    
    def detectar_categoria_inteligente(self, titulo: str, contenido: str = "") -> str:
        """Detecta categoría automáticamente basada en contenido"""
        texto_completo = f"{titulo} {contenido}".lower()
        
        # Mapeo de categorías con keywords
        categorias = {
            'Energía Solar': ['solar', 'fotovoltaica', 'paneles', 'autoconsumo', 'pv'],
            'Tecnología': ['innovación', 'desarrollo', 'avance', 'investigación', 'inteligencia artificial', 'ia'],
            'Noticias Sector': ['mercado', 'industria', 'sector', 'regulación', 'política', 'decreto', 'ley'],
            'Sostenibilidad': ['sostenible', 'verde', 'ambiente', 'carbono', 'clima', 'sustentable'],
            'Instalaciones': ['proyecto', 'instalación', 'construcción', 'planta', 'parque', 'obra']
        }
        
        # Contar matches por categoría
        scores = {}
        for categoria, keywords in categorias.items():
            score = sum(1 for keyword in keywords if keyword in texto_completo)
            if score > 0:
                scores[categoria] = score
        
        # Retornar categoría con mayor score
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return 'Noticias Sector'  # Default
    
    def validar_noticia_calidad(self, noticia: Dict) -> Dict[str, float]:
        """Valida calidad de una noticia generada"""
        scores = {}
        
        # Score de longitud
        contenido_len = len(noticia.get('contenido', ''))
        if 500 <= contenido_len <= 1500:
            scores['longitud'] = 10.0
        elif 300 <= contenido_len <= 2000:
            scores['longitud'] = 8.0
        else:
            scores['longitud'] = 5.0
        
        # Score SEO
        titulo_len = len(noticia.get('titulo', ''))
        desc_len = len(noticia.get('descripcion_corta', ''))
        
        seo_score = 5.0
        if 30 <= titulo_len <= 200:
            seo_score += 2.0
        if 100 <= desc_len <= 300:
            seo_score += 2.0
        if noticia.get('seo', {}).get('meta_keywords'):
            seo_score += 1.0
        
        scores['seo'] = seo_score
        
        # Score de relevancia Argentina
        contenido = noticia.get('contenido', '').lower()
        keywords_argentina = ['argentina', 'renovar', 'empresas', 'autoconsumo', 'inglat']
        relevancia_score = sum(2.0 for kw in keywords_argentina if kw in contenido)
        scores['relevancia_argentina'] = min(relevancia_score, 10.0)
        
        # Score general (promedio)
        scores['score_general'] = sum(scores.values()) / len(scores)
        
        return scores
    
    def cargar_noticias_json(self, archivo_path: str) -> Optional[Dict]:
        """Carga archivo JSON de noticias con manejo de errores"""
        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            self.logger.error(f'Archivo no encontrado: {archivo_path}')
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f'Error parsing JSON {archivo_path}: {str(e)}')
            return None
        except Exception as e:
            self.logger.error(f'Error cargando {archivo_path}: {str(e)}')
            return None
    
    def guardar_noticias_json(self, data: Dict, archivo_path: str) -> bool:
        """Guarda archivo JSON de noticias"""
        try:
            with open(archivo_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.logger.error(f'Error guardando {archivo_path}: {str(e)}')
            return False
    
    def log_operacion(self, operacion: str, resultado: str, detalles: Dict = None):
        """Log estructurado para operaciones Estefani"""
        timestamp = timezone.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'operacion': operacion,
            'resultado': resultado,
            'detalles': detalles or {}
        }
        
        if resultado == 'SUCCESS':
            self.logger.info(f"{operacion}: {resultado} - {json.dumps(detalles, ensure_ascii=False)}")
        else:
            self.logger.error(f"{operacion}: {resultado} - {json.dumps(detalles, ensure_ascii=False)}")


# Instancia global para reutilización
estefani_core = EstefaniCore()