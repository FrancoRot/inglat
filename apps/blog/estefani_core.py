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
    
    # VALIDACIÓN ANTI-ROBÓTICA
    
    def validar_contenido_humano(self, contenido: str, titulo: str = "") -> Dict:
        """Valida que el contenido suene natural y humano"""
        problemas = []
        score_humanidad = 100
        
        # Patrones robóticos a detectar
        patrones_roboticos = [
            r'Análisis especializado sobre',
            r'Contexto regional:',
            r'\d{8}_\d{4}',  # timestamps
            r'se enmarca en un momento',
            r'confluyen factores',
            r'desde INGLAT Argentina',
            r'La información sobre.*se enmarca',
            r'Perspectiva.*del mercado',
        ]
        
        # Revisar patrones robóticos
        for patron in patrones_roboticos:
            import re
            if re.search(patron, contenido, re.IGNORECASE):
                problemas.append(f"Contiene patrón robótico: {patron}")
                score_humanidad -= 15
        
        # Revisar repeticiones excesivas
        palabras = contenido.lower().split()
        from collections import Counter
        contador_palabras = Counter(palabras)
        
        for palabra, count in contador_palabras.most_common(10):
            if len(palabra) > 4 and count > 8:  # Palabra repetida más de 8 veces
                problemas.append(f"Palabra '{palabra}' repetida {count} veces")
                score_humanidad -= 10
        
        # Revisar longitud de párrafos (muy largos son robóticos)
        parrafos = contenido.split('<p>')
        for i, parrafo in enumerate(parrafos[1:], 1):  # Skip primer elemento vacío
            clean_parrafo = re.sub(r'<[^>]+>', '', parrafo)
            if len(clean_parrafo) > 500:
                problemas.append(f"Párrafo {i} muy largo ({len(clean_parrafo)} caracteres)")
                score_humanidad -= 5
        
        # Revisar falta de variación en estructura
        if contenido.count('<strong>') > 6:
            problemas.append("Demasiados elementos <strong> (posible estructura rígida)")
            score_humanidad -= 10
        
        # Calcular score final
        score_humanidad = max(0, score_humanidad)
        
        return {
            'es_humano': score_humanidad >= 70,
            'score_humanidad': score_humanidad,
            'problemas': problemas,
            'recomendaciones': self._generar_recomendaciones(problemas)
        }
    
    def _generar_recomendaciones(self, problemas: List[str]) -> List[str]:
        """Genera recomendaciones específicas basadas en problemas detectados"""
        recomendaciones = []
        
        problemas_text = ' '.join(problemas).lower()
        
        if 'robótico' in problemas_text:
            recomendaciones.append("Usar lenguaje más natural y conversacional")
            recomendaciones.append("Variar las estructuras de introducción")
        
        if 'repetida' in problemas_text:
            recomendaciones.append("Usar sinónimos para evitar repeticiones")
            recomendaciones.append("Reestructurar párrafos para mayor variedad")
        
        if 'largo' in problemas_text:
            recomendaciones.append("Dividir párrafos largos en múltiples párrafos")
            recomendaciones.append("Usar listas o bullets para información densa")
        
        if 'strong' in problemas_text:
            recomendaciones.append("Reducir uso de negritas, usar solo para puntos clave")
            recomendaciones.append("Variar la estructura visual del contenido")
        
        if not recomendaciones:
            recomendaciones.append("Contenido aprobado - mantener este nivel de calidad")
        
        return recomendaciones
    
    # PLANTILLAS OPTIMIZADAS (reutilizables entre comandos)
    
    def get_plantilla_profesional(self, titulo: str, descripcion: str, portal: str) -> str:
        """Plantilla profesional humanizada para generar contenido atractivo"""
        return f"""
Redacta un artículo periodístico profesional y atractivo sobre: "{titulo}"
Fuente: {portal} | Información base: {descripcion}

OBJETIVO: Crear contenido que enganche al lector desde el primer párrafo

ESTRUCTURA NATURAL:
- Párrafo inicial impactante que capture la atención
- Desarrollo del tema con casos concretos y beneficios tangibles  
- Contexto argentino relevante (regulaciones, mercado, oportunidades)
- Perspectiva práctica para empresas argentinas
- Cierre que invite a la acción o reflexión

ESTILO DE REDACCIÓN:
- Tono profesional pero accesible, como un especialista que explica a colegas
- Usa datos concretos y ejemplos reales cuando sea posible
- Evita jerga técnica excesiva - explica conceptos complejos de forma simple
- Incluye beneficios económicos específicos (% de ahorro, ROI, etc.)
- Menciona casos de éxito o tendencias del mercado argentino

LONGITUD: 600-800 palabras
FORMATO: HTML simple (solo <p>, <strong>, <blockquote>)
ENFOQUE: Empresas argentinas interesadas en eficiencia energética
        """.strip()
    
    def get_plantilla_empresarial(self, titulo: str, descripcion: str, portal: str) -> str:
        """Plantilla empresarial humanizada enfocada en resultados"""
        return f"""
Redacta un artículo enfocado en decisores empresariales sobre: "{titulo}"
Fuente: {portal} | Información base: {descripcion}

ENFOQUE: Empresario argentino evaluando inversiones en eficiencia energética

ESTRUCTURA RECOMENDADA:
- Apertura con un dato impactante o estadística relevante
- Explicación clara del tema en términos de negocio (no técnicos)
- Beneficios concretos: ahorro en pesos, reducción de costos, tiempo de retorno
- Casos reales de empresas argentinas similares (si es posible)
- Marco regulatorio favorable en Argentina
- Próximos pasos o llamada a la acción

TONO: Directo, orientado a resultados, con credibilidad técnica pero lenguaje empresarial

ELEMENTOS CLAVE A INCLUIR:
- Cifras de ahorro o beneficios económicos
- Comparación con costos actuales de energía
- Ventajas competitivas para la empresa
- Aspectos de sustentabilidad como valor agregado
- Referencias a incentivos fiscales o regulaciones favorables

LONGITUD: 500-700 palabras
FORMATO: HTML simple, fácil de leer en móvil
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