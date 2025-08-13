#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para poblar la base de datos con contenido de ejemplo para el blog INGLAT
Ejecutar con: python manage.py shell < populate_blog.py
"""

import os
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INGLAT.settings')
django.setup()

from apps.blog.models import Categoria, Noticia

def create_categories():
    """Crea las 5 categorías principales del blog"""
    categorias_data = [
        {
            'nombre': 'Energia Solar',
            'descripcion': 'Ultimas novedades en tecnologia solar fotovoltaica',
            'icono': 'fas fa-solar-panel',
            'color': '#006466',
            'orden': 1
        },
        {
            'nombre': 'Eficiencia Energetica',
            'descripcion': 'Consejos y tecnologias para optimizar el consumo energetico',
            'icono': 'fas fa-leaf',
            'color': '#FF6B35',
            'orden': 2
        },
        {
            'nombre': 'Normativas y Regulacion',
            'descripcion': 'Cambios normativos y regulaciones del sector energetico',
            'icono': 'fas fa-gavel',
            'color': '#1b3a4b',
            'orden': 3
        },
        {
            'nombre': 'Tecnologia e Innovacion',
            'descripcion': 'Innovaciones tecnologicas en energias renovables',
            'icono': 'fas fa-lightbulb',
            'color': '#FFB627',
            'orden': 4
        },
        {
            'nombre': 'Proyectos Realizados',
            'descripcion': 'Casos de exito e instalaciones destacadas',
            'icono': 'fas fa-trophy',
            'color': '#008B8D',
            'orden': 5
        }
    ]
    
    categorias_creadas = []
    for cat_data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults=cat_data
        )
        if created:
            print(f"✓ Categoria creada: {categoria.nombre}")
        else:
            print(f"• Categoria ya existe: {categoria.nombre}")
        categorias_creadas.append(categoria)
    
    return categorias_creadas

def create_articles():
    """Crea 2 artículos de ejemplo"""
    
    # Obtener categorías
    try:
        categoria_normativas = Categoria.objects.get(nombre='Normativas y Regulacion')
        categoria_tecnologia = Categoria.objects.get(nombre='Tecnologia e Innovacion')
    except Categoria.DoesNotExist:
        print("Error: Primero se deben crear las categorías")
        return
    
    # Artículo 1: Incentivos Argentina
    articulo1_data = {
        'titulo': 'Argentina lanza nuevos incentivos fiscales para instalaciones solares residenciales en 2025',
        'descripcion_corta': 'El gobierno argentino anuncia beneficios fiscales históricos para promover la adopción de energía solar en hogares, con deducciones de hasta el 50% en Ganancias.',
        'contenido': '''
El Ministerio de Economía de Argentina anunció oficialmente un paquete de incentivos fiscales sin precedentes para acelerar la adopción de energía solar residencial durante 2025, en línea con los compromisos climáticos del país y la meta de alcanzar el 20% de energías renovables para el año 2025.

## Principales Beneficios Fiscales

### Deducción en Impuesto a las Ganancias
Los contribuyentes podrán deducir hasta el **50% del costo total** de la instalación solar de su declaración anual de Ganancias, con un tope máximo de $3.000.000 por contribuyente. Esta deducción se aplicará en el ejercicio fiscal 2025 y podrá ser utilizada por propietarios de viviendas que instalen sistemas fotovoltaicos certificados.

### Exención del IVA
Las instalaciones solares residenciales estarán **exentas del 21% de IVA** para equipos, componentes y servicios de instalación. Esta medida reduce significativamente el costo inicial y hace más accesible la tecnología solar para familias de clase media.

### Crédito Fiscal Verde
Se estableció un crédito fiscal especial del 15% adicional para instalaciones que incluyan sistemas de almacenamiento en baterías, reconociendo el valor agregado de la autonomía energética completa.

## Requisitos y Condiciones

Para acceder a estos beneficios, las instalaciones deben:

- Contar con **certificación INTI** (Instituto Nacional de Tecnología Industrial)
- Ser instaladas por empresas registradas en el Registro Nacional de Instaladores Solares
- Tener una potencia mínima de 3 kW y máxima de 10 kW por vivienda
- Incluir medición bidireccional para inyección de excedentes a la red

## Impacto Proyectado

El Secretario de Energía proyecta que estas medidas impulsarán la instalación de **25.000 nuevos sistemas residenciales** durante 2025, agregando aproximadamente 150 MW de capacidad distribuida al sistema energético nacional.

"Estimamos que una familia promedio con consumo de 300 kWh mensuales podrá recuperar su inversión en 4-5 años, considerando los incentivos y el ahorro en la factura eléctrica", explicó la Subsecretaria de Energías Renovables.

## Timeline de Implementación

- **Enero 2025**: Publicación de la reglamentación completa
- **Febrero 2025**: Apertura del registro de instaladores certificados
- **Marzo 2025**: Inicio de la recepción de solicitudes de beneficios
- **Diciembre 2025**: Fecha límite para instalaciones que acceden a incentivos 2025

## Cómo INGLAT Te Ayuda

En **INGLAT**, estamos preparados para ayudarte a aprovechar al máximo estos incentivos históricos. Nuestro equipo de ingenieros especializados se encargará de:

- **Asesoría integral**: Calculamos el dimensionamiento óptimo para maximizar tus beneficios fiscales
- **Gestión de trámites**: Nos ocupamos de toda la documentación y certificaciones requeridas
- **Instalación certificada**: Somos instaladores registrados con más de 500 proyectos exitosos
- **Monitoreo avanzado**: Incluimos sistemas de monitorización que optimizan el rendimiento y facilitan los reportes fiscales

### Simulación de Beneficios

Una instalación típica de 5 kW con INGLAT tiene un costo aproximado de $2.500.000. Con los nuevos incentivos:

- Deducción Ganancias (50%): -$1.250.000
- Exención IVA (21%): -$525.000
- **Costo neto final**: $725.000
- **Ahorro mensual estimado**: $35.000
- **Periodo de retorno**: 2.1 años

## Perspectiva de Mercado

Argentina se posiciona como uno de los países latinoamericanos con políticas más agresivas para la transición energética residencial. Estos incentivos coloca al país en línea con programas similares exitosos en México, Brasil y Chile.

El sector privado ya está respondiendo: se estima una inversión de $15.000 millones en nuevas instalaciones solares residenciales durante 2025, generando aproximadamente 8.000 empleos directos e indirectos.

**La ventana de oportunidad es limitada**. Los cupos de beneficios fiscales están sujetos a disponibilidad presupuestaria y se asignarán por orden de presentación de solicitudes.

*¿Estás listo para formar parte de la revolución energética argentina? Contacta a INGLAT hoy y comienza tu camino hacia la independencia energética con el respaldo de los mayores incentivos fiscales de la historia.*
        ''',
        'categoria': categoria_normativas,
        'tipo_multimedia': 'imagen',
        'destacada': True,
        'activa': True,
        'meta_descripcion': 'Argentina anuncia incentivos fiscales históricos para energía solar residencial en 2025: deducción del 50% en Ganancias y exención de IVA.',
        'meta_keywords': 'incentivos solares Argentina 2025, beneficios fiscales energia renovable, deduccion ganancias paneles solares, exencion IVA solar',
        'fecha_publicacion': datetime.now() - timedelta(days=3)
    }
    
    # Artículo 2: Monitoreo Inteligente
    articulo2_data = {
        'titulo': 'Tecnologia de monitoreo inteligente reduce costos de mantenimiento hasta un 30%',
        'descripcion_corta': 'Sistemas de monitorización avanzada con inteligencia artificial están revolucionando el mantenimiento predictivo de instalaciones solares, reduciendo costos operativos significativamente.',
        'contenido': '''
La industria solar está viviendo una revolución silenciosa: los sistemas de **monitoreo inteligente** basados en inteligencia artificial y análisis predictivo están transformando radical mente la gestión y mantenimiento de instalaciones fotovoltaicas, con resultados que superan todas las expectativas del sector.

## La Revolución del Mantenimiento Predictivo

### Datos que Salvan Inversiones

Un estudio realizado por el Instituto Internacional de Energía Solar sobre 10.000 instalaciones monitoreadas durante 24 meses arrojó resultados contundentes:

- **Reducción del 32% en costos de mantenimiento** comparado con mantenimiento programado tradicional
- **Incremento del 18% en la producción energética** a través de detección temprana de problemas
- **Extensión de la vida útil** de los componentes en un promedio de 2.3 años
- **Tiempo de inactividad reducido en 85%** gracias a diagnósticos remotos instantáneos

### Cómo Funciona la Inteligencia Artificial Solar

Los modernos sistemas de monitoreo combinan múltiples tecnologías avanzadas:

#### Análisis en Tiempo Real
- **Sensores IoT**: Más de 50 parámetros monitoreados por segundo
- **Machine Learning**: Algoritmos que aprenden patrones normales y detectan anomalías
- **Visión Artificial**: Análisis automático de imágenes térmicas para detectar puntos calientes
- **Predicción Meteorológica**: Correlación con datos climáticos para optimización proactiva

#### Diagnóstico Inteligente
El sistema identifica automáticamente:
- Degradación gradual de paneles (antes de impactar la producción)
- Fallos inminentes en inversores (con 95% de precisión)
- Sombreado variable por crecimiento de vegetación
- Pérdidas por acumulación de suciedad
- Problemas de conexión en el cableado

## Casos de Estudio Reales

### Caso INGLAT: Complejo Industrial Córdoba

**Instalación**: 500 kW, 1.200 paneles, instalada en 2022

**Situación anterior (mantenimiento tradicional)**:
- Revisiones trimestrales programadas: $180.000/año
- 3 fallas mayores no detectadas: $520.000 en producción perdida
- Tiempo de resolución promedio: 48 horas
- **Costo total anual**: $700.000

**Con monitoreo inteligente INGLAT**:
- Detección automática de 12 problemas menores antes de convertirse en fallas
- 1 sola intervención de emergencia en 18 meses
- Tiempo de resolución promedio: 4 horas
- **Costo total anual**: $220.000
- **Ahorro neto**: $480.000 (68% de reducción)

### Caso Residencial: Barrio Cerrado San Isidro

**Instalación**: 85 viviendas con sistemas de 8 kW promedio

**Resultados en 12 meses**:
- **Producción energética 22% superior** al estimado inicial
- **Cero fallas críticas** no detectadas
- **Mantenimiento preventivo reducido** de 6 a 2 intervenciones anuales
- **Satisfacción del cliente**: 98% (vs 76% con mantenimiento tradicional)

## Tecnologías Disruptivas Implementadas

### Algoritmos de Aprendizaje Profundo

Los sistemas más avanzados utilizan **redes neuronales profundas** entrenadas con millones de datos históricos para:

- Predecir el rendimiento óptimo según condiciones específicas
- Detectar patrones de degradación únicos por modelo de panel
- Optimizar automáticamente la configuración del sistema
- Generar reportes predictivos de performance financiera

### Integración con Sensores Ambientales

**Estaciones meteorológicas integradas** proporcionan:
- Medición de irradiancia solar con precisión de laboratorio
- Detección de calima y contaminación atmosférica
- Análisis de temperatura de células en tiempo real
- Predicción de eventos climáticos adversos

### Dashboard Inteligente Multi-Dispositivo

La plataforma de monitoreo ofrece:
- **Alertas proactivas** vía SMS, email y push notifications
- **Análisis financiero automático** con ROI actualizado diariamente
- **Comparativas de rendimiento** con instalaciones similares
- **Reportes regulatorios** automáticos para cumplimiento normativo

## Impacto Económico Cuantificado

### Análisis de 500 Instalaciones INGLAT (2022-2024)

**Instalaciones con monitoreo básico**:
- Costo de mantenimiento: 2.1% de la inversión inicial anual
- Tiempo de inactividad: 156 horas/año promedio
- Detección de problemas: 65% reactiva, 35% proactiva

**Instalaciones con monitoreo inteligente**:
- Costo de mantenimiento: 0.7% de la inversión inicial anual
- Tiempo de inactividad: 23 horas/año promedio  
- Detección de problemas: 15% reactiva, 85% proactiva

### ROI del Monitoreo Inteligente

Para una instalación típica de $2.000.000:
- **Costo del sistema de monitoreo**: $120.000 (one-time)
- **Ahorro anual promedio**: $84.000
- **Payback period**: 1.4 años
- **Valor agregado en 10 años**: $720.000

## Próximas Innovaciones

### Integración con Blockchain
- Certificación automática de créditos de carbono
- Trazabilidad de la energía renovable producida
- Smart contracts para venta de excedentes

### Realidad Aumentada para Mantenimiento
- Guías visuales superpuestas para técnicos
- Diagnóstico remoto asistido por expertos
- Training automático del personal de mantenimiento

## La Propuesta INGLAT: Monitoreo de Próxima Generación

En **INGLAT**, no solo instalamos paneles solares: **implementamos ecosistemas energéticos inteligentes**. Nuestro sistema de monitoreo incluye:

### Plataforma Propietaria INGLAT Smart Monitor
- **Dashboard personalizado** con KPIs específicos para tu instalación
- **Alertas inteligentes** configurables según tus preferencias
- **Análisis predictivo financiero** con proyecciones actualizadas
- **Integración con sistemas de gestión empresarial** (SAP, ERP)

### Servicio de Mantenimiento Predictivo
- **Técnicos certificados** con acceso remoto a diagnósticos
- **Respuesta en menos de 4 horas** para emergencias críticas
- **Piezas de repuesto gestionadas automáticamente** según predicciones de falla
- **Garantía extendida** respaldada por datos de performance

### Optimización Continua
- **Machine learning personalizado** para tu instalación específica
- **Actualizaciones de software automáticas** sin interrupciones
- **Benchmarking** contra mejores prácticas de la industria
- **Consultoría energética** basada en datos reales de consumo

## Conclusión: El Futuro es Ahora

La diferencia entre una instalación solar tradicional y una **instalación solar inteligente** no es solo tecnológica: es una diferencia de **rentabilidad, tranquilidad y sustentabilidad** a largo plazo.

Los datos son claros: **el monitoreo inteligente no es un lujo, es una necesidad** para cualquier instalación solar que busque maximizar su retorno de inversión y minimizar riesgos operativos.

*¿Tu instalación solar actual está operando a su máximo potencial? ¿Sabes exactamente cuánto dinero podrías estar perdiendo por falta de monitoreo adecuado? En INGLAT, convertimos tus paneles solares en una inversión verdaderamente inteligente.*

**Solicita una evaluación gratuita de tu instalación actual** y descubre cuánto podrías estar ahorrando con tecnología de monitoreo de próxima generación.
        ''',
        'categoria': categoria_tecnologia,
        'tipo_multimedia': 'video',
        'video_vimeo_url': 'https://vimeo.com/showcase/7060635',  # Video educativo sobre monitoreo solar
        'destacada': True,
        'activa': True,
        'meta_descripcion': 'Sistemas de monitoreo inteligente con IA reducen costos de mantenimiento solar hasta 30%. Descubre cómo la tecnología predictiva optimiza instalaciones.',
        'meta_keywords': 'monitoreo inteligente solar, mantenimiento predictivo paneles solares, inteligencia artificial energia renovable, IoT solar',
        'fecha_publicacion': datetime.now() - timedelta(days=1)
    }
    
    # Crear artículos
    articulos_data = [articulo1_data, articulo2_data]
    articulos_creados = []
    
    for art_data in articulos_data:
        articulo, created = Noticia.objects.get_or_create(
            titulo=art_data['titulo'],
            defaults=art_data
        )
        if created:
            print(f"✓ Articulo creado: {articulo.titulo[:50]}...")
        else:
            print(f"• Articulo ya existe: {articulo.titulo[:50]}...")
        articulos_creados.append(articulo)
    
    return articulos_creados

def main():
    """Función principal del script"""
    print("=== POBLANDO BASE DE DATOS DEL BLOG INGLAT ===\n")
    
    print("1. Creando categorías...")
    categorias = create_categories()
    print(f"   Total categorías: {len(categorias)}\n")
    
    print("2. Creando artículos de ejemplo...")
    articulos = create_articles()
    print(f"   Total artículos: {len(articulos)}\n")
    
    # Verificar estado final
    print("=== RESUMEN FINAL ===")
    print(f"Categorías activas: {Categoria.objects.filter(activa=True).count()}")
    print(f"Noticias activas: {Noticia.objects.filter(activa=True).count()}")
    print(f"Noticias destacadas: {Noticia.objects.filter(destacada=True, activa=True).count()}")
    
    print("\n✅ ¡Blog poblado exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Accede al admin de Django: /admin/")
    print("2. Ve al blog: /noticias/")
    print("3. Verifica la página principal con noticias destacadas: /")

if __name__ == "__main__":
    main()