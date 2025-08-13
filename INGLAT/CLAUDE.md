# CLAUDE.md - Guía Completa para Claude Code

Este archivo proporciona orientación completa a Claude Code (claude.ai/code) cuando trabaja con el código en este repositorio.

## 📋 Contexto del Proyecto

**INGLAT** - Empresa de instalaciones y monitorización de energía renovable (fotovoltaica)

### 🏗️ Stack Tecnológico Actualizado
- **Backend**: Django 5.2.4 + Python 3.11+
- **Base de Datos**: PostgreSQL con configuración segura
- **Frontend**: HTML + CSS + JavaScript (Vanilla) con diseño responsive
- **Integración WhatsApp**: Detección inteligente de dispositivos con fallback
- **Email**: SpaceMail SMTP con configuración robusta
- **Control de Versiones**: Git

### 🎯 Fase Actual del Proyecto
Sitio web corporativo completo con simulador de energía solar avanzado, portfolio de proyectos, sistema de contacto integrado con WhatsApp, blog de noticias con categorías, y funcionalidades de SEO optimizadas. Datos específicos de irradiación solar argentina y cálculos de costos regionales. Funcionalidad de dashboard para monitorización de clientes planificada para el futuro.

---

## 📚 Documentación de Referencia - Cuándo Usar Cada Documento

### 🎨 **UI_UX_doc.md** - Guía de Diseño y Experiencia de Usuario
**📖 Cuándo consultar**: Modificaciones de diseño, CSS, experiencia de usuario, componentes visuales
**📋 Contenido**: Paleta de colores INGLAT, tipografía, componentes base, responsive design, accesibilidad
**💡 Ejemplo de uso**: "Si necesitas cambiar colores, crear nuevos componentes, modificar el diseño responsive o implementar nuevas funcionalidades visuales"
**🔗 Ubicación**: `docs/UI_UX_doc.md`

### 🐛 **Bug_tracking.md** - Seguimiento de Errores y Debugging
**📖 Cuándo consultar**: Documentar bugs, reparar código, debugging, problemas de seguridad
**📋 Contenido**: Bugs activos, soluciones aplicadas, debugging tips, errores comunes, checklist pre-commit
**💡 Ejemplo de uso**: "Antes de hacer cambios, revisa si hay bugs conocidos. Al encontrar un problema, documenta la solución aquí"
**🔗 Ubicación**: `docs/Bug_tracking.md`

### 🏗️ **Project_structure.md** - Arquitectura y Estructura del Proyecto
**📖 Cuándo consultar**: Entender la arquitectura, agregar nuevas apps, modificar estructura de directorios
**📋 Contenido**: Stack tecnológico, estructura de directorios, convenciones de código, configuración por entornos
**💡 Ejemplo de uso**: "Para entender cómo está organizado el proyecto, dónde agregar nuevas funcionalidades o modificar la arquitectura"
**🔗 Ubicación**: `docs/Project_structure.md`

### 📋 **PRD.md** - Product Requirements Document
**📖 Cuándo consultar**: Entender requisitos del negocio, funcionalidades del producto, roadmap
**📋 Contenido**: Visión del producto, funcionalidades por fase, criterios de éxito, roadmap de desarrollo
**💡 Ejemplo de uso**: "Para entender qué funcionalidades implementar, prioridades del negocio o criterios de aceptación"
**🔗 Ubicación**: `docs/PRD.md`

### ⚙️ **Implementation.md** - Guía de Implementación
**📖 Cuándo consultar**: Implementar nuevas funcionalidades, entender el estado actual, convenciones de desarrollo
**📋 Contenido**: Estado del proyecto, estructura de apps, URLs principales, convenciones CSS/JS
**💡 Ejemplo de uso**: "Para entender qué está implementado, cómo agregar nuevas funcionalidades o seguir las convenciones del proyecto"
**🔗 Ubicación**: `docs/Implementation.md`

---

## 🚀 Comandos de Desarrollo

### Django Management
```bash
# Servidor de desarrollo
python manage.py runserver

# Crear y aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario para admin
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic

# Acceso al shell
python manage.py shell
```

### Testing
```bash
# Testing de Django integrado
python manage.py test
python manage.py test apps.core
python manage.py test apps.core.tests.TestModelName

# Con coverage (si está instalado)
python manage.py test --coverage

# Recomendado agregar pytest-django para testing avanzado
```

### Operaciones de Base de Datos
```bash
# Reset de base de datos (solo desarrollo)
python manage.py flush

# Cargar fixtures
python manage.py loaddata <fixture_name>

# Shell de base de datos
python manage.py dbshell
```

### Entorno Virtual
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements/base.txt        # Dependencias de producción
pip install -r requirements/development.txt # Dependencias de desarrollo
pip install -r requirements/production.txt  # Dependencias específicas de producción

# O instalar todo de una vez
pip install -r requirements.txt
```

### Calidad de Código y Linting
```bash
# Recomendado agregar y ejecutar regularmente:
# flake8 .                    # Linting de Python
# black .                     # Formateo de código  
# isort .                     # Ordenamiento de imports
# pylint apps/                # Análisis de código

# Verificaciones del sistema Django
python manage.py check
python manage.py check --deploy  # Preparación para producción
```

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Apps Django
- **apps/core**: Aplicación principal - página de inicio, nosotros, servicios, simulador solar y modelos de configuración
- **apps/projects**: Gestión de portfolio de proyectos (usa modelos de core app)
- **apps/blog**: Sistema completo de noticias con categorías, multimedia y SEO
- **apps/contact**: Sistema de contacto multicanal con integración WhatsApp inteligente
- **apps/dashboard**: Funcionalidad futura de dashboard para clientes

### Modelos Principales (apps/core/models.py)
- **Project**: Proyectos de instalación solar con imágenes, descripciones y especificaciones técnicas
- **SimuladorConfig**: Configuración global del simulador de energía solar
- **CostoInstalacion**: Rangos de costos de instalación por capacidad de potencia
- **FactorUbicacion**: Factores de irradiación solar por provincias argentinas
- **FactorOrientacion**: Factores de eficiencia por orientación del tejado
- **TipoTejado**: Tipos de tejado con factores de complejidad
- **AnguloTejado**: Ángulos de inclinación con factores de eficiencia

### Modelos de Blog (apps/blog/models.py)
- **Categoria**: Categorías de noticias con iconos, colores y orden
- **Noticia**: Artículos completos con multimedia (imagen/video), SEO y metadatos

### Modelos de Contacto (apps/contact/models.py)
- **ContactMessage**: Mensajes de contacto con tipos de proyecto y seguimiento interno

### Estructura de URLs
- `/` - Página de inicio (core app)
- `/proyectos/` - Portfolio de proyectos
- `/simulador/` - Simulador de energía solar
- `/noticias/` - Blog de noticias (también `/blog/` por compatibilidad)
- `/contacto/` - Página de contacto
- `/admin/` - Panel de administración de Django

### Organización de Archivos Estáticos
- **CSS**: `static/css/` - Separado por funcionalidad (base.css, header.css, footer.css, home.css, simulador.css, noticias.css)
- **JavaScript**: `static/js/` - Estructura modular (base.js, home.js, contact.js, whatsapp.js, simulador.js, noticias.js)
- **Imágenes**: `static/images/` - Organizado por tipo, incluye iconos SVG del simulador
- **Media**: `media/` - Archivos subidos por usuarios (proyectos, blog)

---

## 🎨 Convenciones de Código

### Python/Django
- Seguir estándares PEP 8
- Comentarios y docstrings en español para colaboración del equipo
- Usar patrón MVT de Django consistentemente
- Variables de entorno para configuraciones sensibles via `get_env_variable()`
- Modelos con nombres verbose en español para interfaz de admin
- Validación apropiada de campos y texto de ayuda en español

### Templates
- Extender desde `templates/base/base.html`
- Usar `{% load static %}` para todas las referencias a archivos estáticos
- Organizar templates por app en `templates/<app_name>/`
- Componentes reutilizables en `templates/base/`

### CSS/JavaScript
- **NO estilos o scripts inline en templates**
- Usar archivos CSS/JS separados por página/funcionalidad
- Estilos globales en `base.css`, estilos específicos en archivos dedicados
- Referenciar en templates con etiquetas static apropiadas:
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/home.css' %}">
<script src="{% static 'js/base.js' %}"></script>
<script src="{% static 'js/home.js' %}"></script>
```

### Base de Datos
- Configuración PostgreSQL via variables de entorno
- Modelos con nombres verbose en español para interfaz de admin
- Usar slugs para URLs amigables para SEO
- Timestamping automático con created_at/updated_at

---

## ⚡ Simulador de Energía Solar

El proyecto incluye un simulador de energía solar comprehensivo con los siguientes componentes:

### Modelos del Simulador
- **SimuladorConfig**: Configuración global para cálculos (eficiencia, precios, factores de autoconsumo)
- **CostoInstalacion**: Costos de instalación por rango de potencia (0-3kW, 3-5kW, 5-10kW, 10+kW)
- **FactorUbicacion**: Irradiación solar por provincias argentinas
- **FactorOrientacion**: Eficiencia por orientación del tejado (N, NE, E, SE, S, SO, O, NO)
- **TipoTejado**: Tipos de tejado con factores de complejidad
- **AnguloTejado**: Ángulos de inclinación con factores de eficiencia

### Funcionalidades del Simulador
- Cálculo de consumo anual
- Dimensionamiento óptimo de potencia
- Estimación de costos de instalación
- Opciones de sistema de baterías
- Integración de vehículo eléctrico
- Cálculos de ROI y tiempo de retorno
- Irradiación solar específica por provincia
- Optimización por tipo y orientación de tejado

### URLs del Simulador
- `/simulador/` - Calculadora solar interactiva
- Endpoint AJAX: `/calcular-solar/` (POST)

---

## 📧 Sistema de Email y Contacto

### Configuración de Email
- **Proveedor**: SpaceMail SMTP
- **Configuración**: SSL en puerto 465, timeout optimizado
- **Fallback**: Backend de consola en desarrollo si no hay credenciales
- **Destinatarios**: Configuración flexible via variables de entorno

### Sistema de Contacto
- **Formulario inteligente**: Detección de dispositivo para integración WhatsApp
- **Tipos de proyecto**: Residencial, comercial, industrial, autoconsumo, baterías, mantenimiento, consultoría
- **Seguimiento interno**: Marcado de leído/respondido, notas internas
- **Validación**: Server-side con manejo de errores robusto

---

## 📰 Sistema de Blog/Noticias

### Funcionalidades Completas
- **Categorías**: Con iconos, colores y orden personalizable
- **Multimedia**: Soporte para imágenes y videos de Vimeo
- **SEO**: Meta descripciones, keywords, URLs amigables
- **Contenido**: Artículos destacados, tiempo de lectura estimado
- **Relacionados**: Noticias relacionadas por categoría
- **Admin**: Gestión completa via Django admin

### URLs del Blog
- `/noticias/` - Lista de noticias (principal)
- `/blog/` - Redirección por compatibilidad
- `/noticias/categoria/<slug>/` - Noticias por categoría
- `/noticias/<slug>/` - Detalle de noticia

---

## 🔧 Ubicaciones de Archivos Importantes

### Configuración
- `INGLAT/settings.py` - Configuración principal de Django
- `requirements/base.txt` - Dependencias principales
- `requirements/development.txt` - Dependencias de desarrollo  
- `requirements/production.txt` - Dependencias de producción
- `requirements.txt` - Archivo principal de requirements

### Documentación
- `docs/PRD.md` - Requisitos del producto y reglas de negocio
- `docs/Project_structure.md` - Documentación detallada de arquitectura
- `docs/UI_UX_doc.md` - Guías de diseño y especificaciones de UI
- `docs/Bug_tracking.md` - Problemas conocidos y reportes de bugs
- `docs/Implementation.md` - Guías de implementación
- `docs/WhatsApp_Integration.md` - Documentación de integración WhatsApp

### Apps Principales
- `apps/core/models.py` - Definición de modelos principales (lógica de negocio principal)
- `apps/core/views.py` - Página de inicio y funcionalidad principal
- `apps/blog/models.py` - Modelos completos del sistema de noticias
- `apps/contact/models.py` - Modelos del sistema de contacto
- `INGLAT/urls.py` - Configuración principal de enrutamiento de URLs

---

## 🔄 Flujo de Desarrollo

### Antes de Hacer Cambios
1. Leer documentación relevante desde directorio `docs/`
2. Verificar `docs/Bug_tracking.md` para problemas conocidos
3. Revisar `docs/UI_UX_doc.md` para guías de diseño
4. Entender reglas de negocio en `docs/PRD.md`
5. Para funcionalidades WhatsApp, consultar `docs/WhatsApp_Integration.md`

### Consideraciones de Seguridad
- Verificar `docs/Bug_tracking.md` para problemas críticos de seguridad
- Nunca commitear datos sensibles (passwords, keys) con valores por defecto
- Validar todas las entradas de usuario en endpoints del calculador
- Usar variables de entorno para todas las configuraciones sensibles

### Desarrollo CSS/JS
- Siempre usar archivos separados, nunca inline
- Actualizar `base.css` para estilos globales y variables CSS
- Crear archivos específicos por página para funcionalidad única
- Probar diseño responsive en todos los dispositivos
- Seguir esquema de colores y branding de INGLAT

### Desarrollo Django
- Usar Django admin para gestión de contenido
- Seguir patrón MVT estrictamente
- Nombres de campos en español y texto de ayuda para usuarios de admin
- Nombrado apropiado de URLs y reverse lookups
- Optimizar para SEO y performance

### Testing
- Probar todos los formularios e interacciones de usuario
- Verificar diseño responsive en móvil/tablet
- Verificar funcionalidad de Django admin para gestión de contenido
- Validar meta tags SEO y schema markup
- Probar calculador solar con varias combinaciones de entrada
- Verificar que endpoints AJAX retornen respuestas JSON válidas

---

## ⚠️ Problemas Conocidos y Consideraciones

### Problemas Críticos (ver docs/Bug_tracking.md)
- Configuración DEBUG debe ser False en producción
- Credenciales de base de datos deben estar en variables de entorno
- SECRET_KEY debe ser configurada sin valor por defecto
- Configuración de MEDIA_URL/MEDIA_ROOT requerida para ImageField
- Validación de entrada faltante en endpoints del calculador

### Dependencias
- `python-decouple` instalado pero no usado (considerar usar para mejor manejo de variables de entorno)
- `django-environ` disponible para gestión de variables de entorno
- No hay framework de testing configurado (recomendar agregar pytest-django)
- Adaptador PostgreSQL: `psycopg2-binary` para conectividad de base de datos
- Pillow para manejo de imágenes en portfolio de proyectos

### Configuración Regional
- Proyecto orientado al mercado argentino (provincias, números de teléfono)
- Datos de irradiación solar específicos de Argentina
- Cálculos de moneda en USD
- Configuración de zona horaria: America/Argentina/Buenos_Aires

---

## 🎯 Funcionalidades Implementadas vs Planificadas

### ✅ Completado
- Setup inicial Django 5.2.4+
- Estructura de apps completa
- Sistema de proyectos con portfolio
- Simulador de energía solar avanzado
- Sistema de contacto con WhatsApp
- Blog de noticias completo con categorías
- Configuración de email robusta
- Documentación completa

### 🔄 En Desarrollo
- Optimización de performance
- Testing automatizado
- Mejoras de SEO

### ⏳ Pendiente
- Dashboard de clientes
- Sistema de monitorización
- App móvil complementaria
- Deploy en producción

---

## 📞 Información de Contacto del Proyecto

- **Email**: info@inglat.com
- **WhatsApp**: +54 11 6721-4369
- **Ubicación**: Argentina
- **Tecnologías**: Django, PostgreSQL, JavaScript, CSS3

---

**Nota**: Este archivo se actualiza regularmente. Siempre consultar la documentación específica en `docs/` para información detallada y actualizada.