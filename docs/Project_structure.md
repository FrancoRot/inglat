
# Project_structure.md - Arquitectura INGLAT

## 🛠️ Stack Tecnológico

### Backend
- **Django 5.2.4** + Python 3.11+ + PostgreSQL
- **Variables de entorno**: python-decouple
- **Email**: SpaceMail SMTP + console fallback

### Frontend  
- **Templates Django** + CSS3 + Vanilla JS
- **Arquitectura modular**: variables CSS, archivos separados
- **Icons**: SVG personalizados

### Herramientas
- **Git + GitHub** - Control de versiones
- **Django Debug Toolbar** - Desarrollo
- **Claude Code** - Agentes especializados

---

## 📁 Estructura Simplificada

```
codigo/
├── INGLAT/                     # Configuración Django
│   ├── settings.py             # Configuración principal
│   ├── urls.py                 # URLs principales
│   └── CLAUDE.md              # Guía de desarrollo
├── apps/                       # Aplicaciones Django
│   ├── core/                   # Home + simulador solar
│   ├── projects/               # Portfolio
│   ├── blog/                   # Noticias  
│   ├── contact/                # Formularios + WhatsApp
│   └── dashboard/              # Futuro
├── templates/                  # Templates HTML
│   ├── base/                   # Layouts base
│   ├── core/                   # Home, simulador
│   ├── projects/               # Portfolio
│   └── contact/                # Contacto
├── static/                     # Archivos estáticos
│   ├── css/                    # Estilos modulares
│   ├── js/                     # Scripts separados
│   └── images/                 # Imágenes + SVG
├── media/                      # Uploads usuarios
├── docs/                       # Documentación
└── requirements.txt            # Dependencias
```

## ⚙️ Configuración

### Entornos
- **Development**: DEBUG=True, Django Debug Toolbar
- **Production**: DEBUG=False, Redis cache, HTTPS

### Dependencias Principales
- **Django 5.2.4** + PostgreSQL + python-decouple
- **Pillow** para imágenes
- **psycopg2** para PostgreSQL

---

## 🔧 Apps Django

### Core App
- **Home**: Hero section + servicios + proyectos destacados
- **Simulador Solar**: Wizard 5 pasos con datos Argentina
- **Modelos**: Project, SimuladorConfig, FactorUbicacion, etc.

### Projects App  
- **Portfolio**: Galería instalaciones realizadas
- **Gestión**: Admin + templates + URLs con slug

### Blog App
- **Noticias**: Categorías + multimedia + SEO
- **Modelos**: Categoria, Noticia

### Contact App
- **Formularios**: Tipos de proyecto + validación
- **WhatsApp**: Integración inteligente por dispositivo

---

## 📋 Convenciones

### Python/Django
- **PEP 8**, comentarios en español
- **Variables de entorno** para configuraciones sensibles
- **MVT pattern** consistente

### CSS/JS
- **Archivos separados** por funcionalidad (NO inline)
- **Variables CSS** en `base.css`
- **Nomenclatura**: `base.css` + específicos por página

### URLs Principales
- `/` - Home + simulador
- `/proyectos/` - Portfolio  
- `/noticias/` - Blog
- `/contacto/` - Formularios

### Ejemplo Template
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/home.css' %}">
```

---

## 📚 Referencias

**📋 Documentación detallada**:
- `Implementation.md` - Estado actual y convenciones completas
- `UI_UX_doc.md` - Variables CSS y componentes  
- `Bug_tracking.md` - Bugs activos y debugging
- `PRD.md` - Requisitos de producto