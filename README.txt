INGLAT - Plataforma Web de Energía Renovable
=============================================

DESCRIPCIÓN:
INGLAT es una empresa especializada en instalaciones y monitorización de sistemas de energía renovable fotovoltaica en Argentina. Esta plataforma web corporativa ofrece servicios de simulación de instalaciones solares, portfolio de proyectos realizados, sistema de contacto integrado con WhatsApp, y blog de noticias del sector energético.

La plataforma está optimizada específicamente para el mercado argentino, incluyendo datos de irradiación solar por provincia, costos de instalación locales, y regulaciones energéticas nacionales.

REQUISITOS DEL SISTEMA:
======================
- Python 3.11+
- Django 5.2.4
- PostgreSQL 12+ (para producción)
- SQLite3 (para desarrollo)
- Node.js/npm (opcional, para herramientas de desarrollo)

DEPENDENCIAS PYTHON:
===================
- asgiref==3.9.1
- beautifulsoup4==4.12.3
- Django==5.2.4
- django-cleanup==9.0.0
- django-tinymce==4.1.0
- lxml==5.3.0
- pillow==11.3.0
- psycopg2-binary==2.9.10
- python-decouple==3.8
- requests==2.32.3
- sqlparse==0.5.3
- tzdata==2025.2

INSTALACIÓN:
============

1. Clonar el repositorio:
   git clone [URL_DEL_REPOSITORIO]
   cd codigo

2. Crear entorno virtual:
   python -m venv venv

   # En Windows:
   venv\Scripts\activate

   # En Linux/Mac:
   source venv/bin/activate

3. Instalar dependencias:
   pip install -r requirements.txt

4. Configurar variables de entorno:
   Copiar env.example a .env y configurar:

   SECRET_KEY=tu_clave_secreta_django_aqui
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Base de datos (desarrollo - SQLite por defecto)
   DATABASE_URL=sqlite:///db.sqlite3

   # Para producción - PostgreSQL:
   DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/inglat_db

   # Configuración email (SpaceMail)
   EMAIL_HOST=mail.spacemail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=tu_usuario@inglat.com
   EMAIL_HOST_PASSWORD=tu_contraseña
   DEFAULT_FROM_EMAIL=contacto@inglat.com

5. Ejecutar migraciones:
   python manage.py migrate

6. Crear superusuario (opcional):
   python manage.py createsuperuser

7. Cargar datos iniciales del simulador:
   python manage.py loaddata fixtures/simulador_inicial.json

8. Recopilar archivos estáticos:
   python manage.py collectstatic

USO:
====

Servidor de desarrollo:
   python manage.py runserver

   Acceder a: http://localhost:8000

Administración Django:
   http://localhost:8000/admin/

Endpoints principales:
   /               - Página principal con simulador
   /noticias/      - Blog de noticias
   /proyectos/     - Portfolio de instalaciones
   /contacto/      - Formulario de contacto
   /simulador/     - Simulador solar interactivo

ESTRUCTURA DEL PROYECTO:
========================

INGLAT/                     # Configuración principal Django
├── settings.py            # Configuración del proyecto
├── urls.py               # URLs principales
└── wsgi.py               # Configuración WSGI

apps/                       # Aplicaciones Django modulares
├── core/                  # App principal (home, simulador)
│   ├── models.py         # Modelos del simulador solar
│   ├── views.py          # Vistas principales
│   └── admin.py          # Configuración admin
├── blog/                  # Sistema de noticias
│   ├── models.py         # Modelos Noticia, Categoria
│   ├── views.py          # Vistas del blog
│   └── management/       # Comandos EstefaniPUBLI
├── contact/               # Sistema de contacto
│   ├── models.py         # Modelo ContactoConsulta
│   ├── forms.py          # Formularios
│   └── views.py          # Procesamiento emails
├── projects/              # Portfolio proyectos
└── dashboard/             # Futuro panel clientes

templates/                  # Templates Django
├── base/                  # Plantillas base
├── core/                  # Templates página principal
├── blog/                  # Templates blog
├── contact/               # Templates contacto
└── emails/                # Templates email

static/                     # Archivos estáticos
├── css/                   # Estilos modulares
├── js/                    # JavaScript modular
├── images/                # Imágenes y SVG
└── fonts/                 # Fuentes web

media/                      # Uploads usuarios
├── noticias/              # Multimedia blog
├── projects/              # Imágenes proyectos
└── videos/                # Videos portada

docs/                       # Documentación técnica
├── PRD.md                 # Especificaciones producto
├── Implementation.md      # Estado implementación
├── UI_UX_doc.md          # Guía diseño/CSS
├── Project_structure.md   # Arquitectura técnica
└── Bug_tracking.md        # Seguimiento bugs

FUNCIONALIDADES PRINCIPALES:
============================

1. SIMULADOR SOLAR:
   - Cálculo de potencia requerida basado en consumo
   - Datos de irradiación por provincia argentina
   - Estimación de costos e instalación
   - ROI y análisis de ahorro energético
   - Configuración de orientación y tipo de tejado

2. BLOG DE NOTICIAS:
   - Sistema de categorías temáticas
   - Multimedia (imágenes/videos) multipla plataforma
   - SEO optimizado con meta tags
   - Noticias destacadas en homepage
   - Integración EstefaniPUBLI (automatización)

3. PORTFOLIO PROYECTOS:
   - Galería de instalaciones realizadas
   - Filtros por tipo cliente y potencia
   - Detalles técnicos y beneficios

4. SISTEMA CONTACTO:
   - Formulario web con validación
   - Integración WhatsApp automática
   - Notificaciones email SpaceMail
   - Tipos de proyecto predefinidos

5. PANEL ADMINISTRATIVO:
   - Gestión contenido blog
   - Configuración simulador
   - Seguimiento consultas
   - Estadísticas de uso

COMANDOS ÚTILES:
===============

Desarrollo:
   python manage.py check              # Verificar proyecto
   python manage.py makemigrations     # Crear migraciones
   python manage.py migrate            # Aplicar migraciones
   python manage.py shell              # Shell interactivo

Producción:
   python manage.py check --deploy     # Verificar config producción
   python manage.py collectstatic      # Recopilar estáticos
   python manage.py compress           # Comprimir CSS/JS (si configurado)

EstefaniPUBLI (Automatización Blog):
   python manage.py estefani_workflow     # Workflow completo
   python manage.py estefani_analizar     # Analizar fuentes
   python manage.py estefani_publicar     # Publicar noticias

CONFIGURACIÓN PRODUCCIÓN:
========================

1. Variables de entorno requeridas:
   DEBUG=False
   SECRET_KEY=[clave-segura-larga]
   ALLOWED_HOSTS=inglat.com,www.inglat.com
   DATABASE_URL=postgresql://...
   EMAIL_HOST_USER=...
   EMAIL_HOST_PASSWORD=...

2. Configuraciones de seguridad:
   - HTTPS obligatorio
   - Cookies seguras
   - HSTS headers
   - CSP policies

3. Optimizaciones:
   - Compresión Gzip
   - CDN para archivos estáticos
   - Cache Redis/Memcached
   - Optimización base de datos

TESTING:
========

Ejecutar tests:
   python manage.py test

Tests de cobertura:
   coverage run manage.py test
   coverage report

CONTRIBUIR:
===========

1. Seguir PEP 8 para código Python
2. Comentarios en español
3. CSS en archivos separados (NO inline)
4. JavaScript modular en static/js/
5. Revisar Bug_tracking.md antes de commits
6. Actualizar documentación si es necesario

ARQUITECTURA:
=============

Frontend:
- Django Templates con herencia
- CSS3 modular + variables CSS
- Vanilla JavaScript (sin frameworks)
- Bootstrap 5 para componentes
- FontAwesome para iconografía

Backend:
- Django 5.2.4 MVT pattern
- PostgreSQL con índices optimizados
- Arquitectura modular por apps
- APIs REST para simulador
- Integración servicios externos

CONTACTO:
=========

Empresa: INGLAT Argentina
Email: contacto@inglat.com
Teléfono: +54 11 6721-4369
Sitio: https://www.inglat.com

Soporte técnico: equipo.desarrollo@inglat.com

LICENCIA:
=========

Código propietario - INGLAT Argentina
Todos los derechos reservados.

ÚLTIMA ACTUALIZACIÓN:
====================

Versión: 1.0.0
Fecha: Septiembre 2024
Estado: Desarrollo completado - Listo para testing pre-producción