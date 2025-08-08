
## Stack Tecnológico

### Backend
- **Framework**: Django 5.2.4
- **Lenguaje**: Python 3.11+
- **Base de Datos**: PostgreSQL
- **Cache**: Redis (opcional para producción)
- **Media Storage**: Django FileField + hostinger VPS (produccion)

### Frontend
- **Templates**: Django Templates
- **CSS**: CSS3 con arquitectura modular (variables CSS, BEM methodology)
- **JavaScript**: Vanilla JS para interactividad
- **Icons**: SVG personalizados + Font Awesome
- **Fonts**: Google Fonts
- **Simulador**: Wizard interactivo de 5 pasos con cálculos solares

### DevOps & Tools
- **Versionado**: Git + GitHub
- **CI/CD**: GitHub Actions
- **Monitoring**: Django Debug Toolbar (dev)
- **Testing**: Django TestCase + Pytest
- **Agentes IA**: Claude Code con agentes especializados (GuidoCODE, ZanganoWEB, inglat-ui-designer)
- **Integración**: WhatsApp Business API

---

## Estructura de Directorios

```
codigo/
├── manage.py
├── requirements.txt             # Archivo principal de dependencias
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── INGLAT/                     # Proyecto principal Django
│   ├── __init__.py
│   ├── settings.py             # Configuración unificada
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── CLAUDE.md              # Documentación para Claude
│   └── todo.md                # Lista de tareas
├── .claude/                    # Configuración de agentes Claude
│   └── agents/
│       ├── GuidoCODE.md       # Agente especializado en desarrollo
│       ├── GuidoCODE.json
│       ├── ZanganoWEB.md      # Agente especializado en web
│       ├── ZanganoWEB.json
│       ├── inglat-ui-designer.md  # Agente especializado en UI/UX
│       └── inglat-ui-designer.json
├── shared_memory/              # Memoria compartida del proyecto
│   ├── architecture_decisions.json
│   ├── development_log.json
│   ├── research_data.json
│   └── setup_check.py
├── apps/                       # Aplicaciones Django
│   ├── __init__.py
│   ├── core/                   # App principal con simulador solar
│   │   ├── __init__.py
│   │   ├── models.py          # Incluye modelos del simulador
│   │   ├── views.py           # Vista SimuladorSolarView
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── migrations/
│   │       ├── 0001_initial.py
│   │       └── 0002_angulotejado_costoinstalacion_factororientacion_and_more.py
│   ├── projects/               # Gestión de proyectos
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── serializers.py
│   ├── blog/                   # Sistema de blog
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── forms.py
│   ├── contact/                # Sistema de contacto
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── utils.py
│   └── dashboard/              # Dashboard clientes (futuro)
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       └── urls.py
├── templates/                  # Templates Django
│   ├── base/
│   │   ├── base.html
│   │   ├── header.html
│   │   └── footer.html
│   ├── core/
│   │   ├── home.html
│   │   ├── simulador.html     # Template del simulador solar
│   │   ├── about.html
│   │   └── services.html
│   ├── projects/
│   │   ├── project_list.html
│   │   └── project_detail.html
│   ├── blog/
│   │   ├── blog_list.html
│   │   └── blog_detail.html
│   └── contact/
│       └── contact.html
├── static/                     # Archivos estáticos
│   ├── css/
│   │   ├── base.css           # Estilos base con variables UI/UX INGLAT
│   │   ├── header.css         # Estilos del header
│   │   ├── footer.css         # Estilos del footer
│   │   ├── home.css           # Estilos específicos del home
│   │   ├── simulador.css      # Estilos del simulador solar
│   │   └── whatsapp-fix.css   # Estilos de integración WhatsApp
│   ├── js/
│   │   ├── base.js            # JavaScript base global
│   │   ├── home.js            # Scripts específicos del home
│   │   ├── simulador.js       # Lógica completa del simulador
│   │   └── whatsapp.js        # Integración con WhatsApp
│   ├── images/
│   │   ├── projects/          # Imágenes de proyectos
│   │   └── simulador/         # Imágenes SVG del simulador
│   │       ├── angulo-0.svg
│   │       ├── angulo-15.svg
│   │       ├── angulo-30.svg
│   │       ├── angulo-45.svg
│   │       ├── angulo-60.svg
│   │       ├── coche-electrico.svg
│   │       ├── sistema-baterias.svg
│   │       ├── tejado-cuatro-aguas.svg
│   │       ├── tejado-dos-aguas.svg
│   │       ├── tejado-plano.svg
│   │       └── tejado-un-agua.svg
│   └── fonts/                 # Fuentes personalizadas (vacío)
├── media/                      # Archivos subidos
│   ├── projects/
│   │   └── images/            # Imágenes de proyectos subidas
│   ├── blog/
│   └── uploads/
├── docs/                       # Documentación
│   ├── PRD.md
│   ├── Project_structure.md
│   ├── Implementation.md
│   ├── UI_UX_doc.md
│   ├── Bug_tracking.md
│   └── WhatsApp_Integration.md
└── venv/                       # Entorno virtual Python
```

## Configuración por Entornos

### Development
- DEBUG = True
- PostgreSQL database
- Django Debug Toolbar
- Static files servidos por Django

### Production
- DEBUG = False
- PostgreSQL database
- Redis cache
- Static files en CDN/S3
- HTTPS obligatorio
- Logging configurado

---

## Dependencias Principales

### Base
```txt
Django==5.2.4
Pillow>=10.0.0
python-decouple>=3.6
django-environ>=0.9.0
psycopg2>=2.9.0
```

### Development
```txt
django-debug-toolbar>=4.0.0
pytest-django>=4.5.0
black>=23.0.0
flake8>=6.0.0
```

### Production
```txt
gunicorn>=20.1.0
psycopg2>=2.9.0
redis>=4.5.0
boto3>=1.26.0  # Para S3
```

---

## Funcionalidades Principales

### Simulador Solar Interactivo
El simulador solar es la funcionalidad principal del sitio, implementado como un wizard de 5 pasos:

**Modelos de Base de Datos:**
- `SimuladorConfig`: Configuración global del simulador
- `CostoInstalacion`: Costos por rangos de potencia (0-3kW, 3-5kW, 5-10kW, 10+kW)
- `FactorUbicacion`: Factores de irradiación por provincias argentinas (24 provincias)
- `FactorOrientacion`: Eficiencia por orientación (N, NE, E, SE, S, SO, O, NO)
- `TipoTejado`: Tipos de tejado con factores de complejidad
- `AnguloTejado`: Ángulos de inclinación con factores de eficiencia

**Wizard de 5 Pasos:**
1. **Consumo**: Selección de consumo mensual en kWh
2. **Ubicación**: Selección de provincia argentina
3. **Orientación**: Orientación del tejado (8 direcciones)
4. **Tipo de Tejado**: Selección visual con SVGs (plano, dos aguas, cuatro aguas, un agua)
5. **Ángulo**: Selección de ángulo de inclinación (0°, 15°, 30°, 45°, 60°)

**Resultados del Simulador:**
- Potencia recomendada del sistema
- Cantidad de paneles necesarios
- Costo estimado de instalación
- Ahorro mensual estimado
- Tiempo de recuperación de la inversión
- Generación mensual esperada

**Archivos Relacionados:**
- `/static/js/simulador.js`: Lógica completa del simulador
- `/static/css/simulador.css`: Estilos específicos
- `/templates/core/simulador.html`: Template del wizard
- `/static/images/simulador/`: Imágenes SVG interactivas

### Sistema de Agentes Claude
Configuración de agentes especializados para desarrollo:
- **GuidoCODE**: Agente especializado en desarrollo y arquitectura
- **ZanganoWEB**: Agente especializado en búsqueda web e información
- **inglat-ui-designer**: Agente especializado en UI/UX y diseño

### Integración WhatsApp
Sistema de integración con WhatsApp Business API para:
- Contacto directo desde simulador
- Envío de resultados de simulación
- Seguimiento de leads generados

---

## Convenciones de Código

### Python/Django
- PEP 8 compliance
- Nombres de clases en PascalCase
- Nombres de variables y funciones en snake_case
- Docstrings en español para funciones complejas
- Type hints donde sea apropiado

### Templates
- Nombres de archivos en snake_case
- Indentación de 2 espacios
- Comentarios en español
- Blocks descriptivos

### CSS/JS
- BEM methodology para CSS
- Prefijos vendor cuando sea necesario
- Comentarios en español
- Archivos separados por funcionalidad

---

## Convenciones para CSS y JS

- Utiliza `static/css/base.css` y `static/js/base.js` para estilos y scripts globales.
- **IMPLEMENTADO**: Archivos separados por funcionalidad:
  - `static/css/header.css`, `static/css/footer.css`, `static/css/home.css`, `static/css/simulador.css`, `static/css/whatsapp-fix.css`
  - `static/js/home.js`, `static/js/simulador.js`, `static/js/whatsapp.js`
- **IMPLEMENTADO**: Variables CSS con paleta de colores INGLAT en `base.css`
- **IMPLEMENTADO**: Imágenes SVG interactivas para el simulador en `static/images/simulador/`
- No uses estilos ni scripts inline en los HTML.
- Referencia los archivos en los templates con `{% load static %}` y las etiquetas `<link>` y `<script>`.

### Ejemplo de referencia en un template:
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/simulador.css' %}">
<script src="{% static 'js/base.js' %}"></script>
<script src="{% static 'js/simulador.js' %}"></script>
```

### URLs y Rutas Principales
- `/`: Página principal (HomeView)
- `/simulador/`: Simulador solar interactivo (SimuladorSolarView)
- `/projects/`: Lista de proyectos
- `/blog/`: Sistema de blog (futuro)
- `/contact/`: Formulario de contacto

- Comenta y etiqueta el código en español.
- Si cambias la estructura, actualiza esta documentación.

---