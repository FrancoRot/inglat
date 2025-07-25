# Implementation Guide

## Estado del Proyecto

### ✅ Completado
- Setup inicial Django 4.2+
- Estructura de apps básica
- Documentación completa

### 🔄 En Desarrollo  
- Templates HTML con nueva paleta
- Sistema de Projects (portfolio)
- Página Nosotros (información corporativa)
- Contact system
- Blog functionality

### ⏳ Pendiente

- Deploy en producción

---

## Apps Django - Estructura

### 1. Core App
**Propósito**: Páginas principales del sitio corporativo  
**Páginas**:
- **Home**: Hero section, servicios destacados, proyectos featured
- **Nosotros**: Quiénes somos, misión, visión, valores, equipo, certificaciones
- **Servicios**: Instalaciones fotovoltaicas, mantenimiento, monitorización, consultoría
**Templates**: `home.html`, `about.html`, `services.html`  
**URLs**: `/`, `/nosotros/`, `/servicios/`

### 2. Projects App  
**Propósito**: Portfolio de instalaciones realizadas  
**Modelos**: `Project` (título, ubicación, potencia, imágenes, tipo)  
**Funcionalidad**: Lista filtrable, detalle proyecto, gestión admin  
**URLs**: `/proyectos/`, `/proyectos/<slug>/`

### 3. Contact App
**Propósito**: Sistema de contacto multi-canal  
**Modelos**: `ContactMessage` (nombre, email, teléfono, tipo consulta, mensaje)  
**Funcionalidad**: Formulario, envío emails, integración WhatsApp  
**URLs**: `/contacto/`

### 4. Blog App
**Propósito**: Blog de noticias sobre energía renovable  
**Estado**: Básico para empezar  
**Modelos**: `BlogPost` (título, contenido, autor, imagen, fecha)  
**URLs**: `/blog/`, `/blog/<slug>/`

---

## URLs Principales
```python
# inglat/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('proyectos/', include('apps.projects.urls')),  
    path('contacto/', include('apps.contact.urls')),
    path('blog/', include('apps.blog.urls')),
]
```

---

## Settings - Apps Instaladas
```python
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps locales
    'apps.core',
    'apps.projects',
    'apps.contact',
    'apps.blog',
]

# Configuración básica
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
DEFAULT_FROM_EMAIL = 'noreply@inglat.com'
```

### Enfoque Actual:
- **Sitio corporativo profesional** 
- **Generación de confianza** (página Nosotros clave)
- **Portfolio atractivo** para mostrar experiencia
- **Contacto multi-canal** para leads

### Contenido Necesario:
- **Textos corporativos** (misión, visión, valores)
- **Fotos del equipo** y instalaciones
- **Certificados y licencias** escaneados
- **Casos de éxito** con datos reales

### Referencias:
- **Estilos CSS**: Ver `UI_UX_doc.md` (paleta INGLAT)
- **Arquitectura**: Ver `Project_structure.md`  
- **Errores**: Ver `Bug_tracking.md`

**Nota**: El código fuente está en los archivos .py. Este documento mantiene solo el estado y referencias del proyecto.

---

## Convenciones para CSS y JS

### Organización de Archivos
- Utiliza un archivo global `base.css` y `base.js` para estilos y scripts compartidos en todo el sitio.
- Para estilos o scripts específicos de una página o app, crea archivos separados en `static/css/` y `static/js/` (ejemplo: `static/css/home.css`, `static/js/home.js`).
- No incluyas estilos ni scripts inline en los archivos HTML. Todo debe estar en archivos separados y correctamente referenciados.

### Referencia en Templates
- En cada template HTML, incluye los archivos CSS y JS correspondientes usando `{% load static %}` y las etiquetas `<link>` y `<script>`:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/home.css' %}">
<script src="{% static 'js/base.js' %}"></script>
<script src="{% static 'js/home.js' %}"></script>
```

### Ejemplo de Organización
- Para la página principal (`home.html`):
  - Estilos globales en `base.css`.
  - Estilos específicos en `home.css`.
  - Scripts globales en `base.js`.
  - Scripts específicos en `home.js`.

### Reglas para Nuevos Estilos y Scripts
- Siempre que crees una nueva página o funcionalidad, crea y referencia sus archivos CSS/JS específicos.
- Si un estilo o script es reutilizable, muévelo a `base.css` o `base.js`.
- Etiqueta y comenta el código en español.
- Actualiza esta documentación si cambias la estructura o agregas nuevas convenciones.

---