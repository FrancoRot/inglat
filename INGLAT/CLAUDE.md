# CLAUDE.md - Guía de Desarrollo INGLAT

Guía específica para Claude Code trabajando en el proyecto INGLAT.

## 📋 Contexto del Proyecto

**INGLAT** - Empresa de instalaciones y monitorización de energía renovable (fotovoltaica)

### 🎯 Objetivo Actual
Sitio web corporativo con simulador de energía solar, portfolio de proyectos, sistema de contacto con WhatsApp, y blog de noticias. Optimizado para Argentina con datos de irradiación solar regionales.

**Stack**: Django 5.2.4 + PostgreSQL + Vanilla JS + CSS3

---

## 📚 Documentación de Referencia

### 🎨 **UI_UX_doc.md** - Diseño y CSS
**Uso**: Colores, tipografía, componentes, responsive design
**Ubicación**: `docs/UI_UX_doc.md`

### 🐛 **Bug_tracking.md** - Bugs y Debugging  
**Uso**: Bugs activos, errores comunes, checklist pre-commit
**Ubicación**: `docs/Bug_tracking.md`

### 🏗️ **Project_structure.md** - Arquitectura
**Uso**: Stack tecnológico, estructura de apps, convenciones
**Ubicación**: `docs/Project_structure.md`

### 📋 **PRD.md** - Requisitos del Producto
**Uso**: Funcionalidades, roadmap, criterios de negocio
**Ubicación**: `docs/PRD.md`

### ⚙️ **Implementation.md** - Estado Actual
**Uso**: Apps implementadas, URLs, convenciones CSS/JS
**Ubicación**: `docs/Implementation.md`

---

## 🚀 Comandos Principales

### Django Básico
```bash
python manage.py runserver           # Servidor desarrollo
python manage.py makemigrations     # Crear migraciones
python manage.py migrate            # Aplicar migraciones
python manage.py collectstatic      # Archivos estáticos
python manage.py check              # Verificar configuración
```

### Entorno
```bash
source venv/bin/activate             # Activar venv (Linux/Mac)
venv\Scripts\activate                # Activar venv (Windows)
pip install -r requirements.txt     # Instalar dependencias
```

---

## 🏗️ Arquitectura Resumida

### Apps Django
- **core**: Home, simulador solar, modelos principales
- **projects**: Portfolio de instalaciones
- **blog**: Noticias con categorías y multimedia
- **contact**: Formularios + WhatsApp integration
- **dashboard**: Planificado para futuro

### URLs Principales  
- `/` - Homepage con simulador
- `/proyectos/` - Portfolio
- `/noticias/` - Blog
- `/contacto/` - Contacto
- `/admin/` - Administración

### Archivos Estáticos
- `static/css/` - Estilos por funcionalidad
- `static/js/` - Scripts modulares
- `static/images/` - Imágenes y SVG
- `media/` - Uploads de usuarios

**📋 Ver Project_structure.md para detalles completos**

---

## 🎨 Convenciones Esenciales

### CSS/JavaScript
- **NO estilos inline** - archivos separados en `static/`
- `base.css` para globales, archivos específicos por página
- Usar `{% load static %}` en templates

### Django
- PEP 8, comentarios en español
- Variables de entorno para configuraciones sensibles
- Modelos con nombres verbose en español

**📋 Ver Implementation.md para convenciones completas**

---

## ⚡ Funcionalidades Clave

### Simulador Solar
- Modelos: SimuladorConfig, CostoInstalacion, FactorUbicacion
- Cálculos: Consumo, potencia, ROI, irradiación por provincia
- URL: `/simulador/` + AJAX `/calcular-solar/`

### Sistema Contacto
- Email: SpaceMail SMTP con fallback console
- WhatsApp: Detección automática de dispositivo
- Tipos: Residencial, comercial, industrial, etc.

### Blog/Noticias
- URLs: `/noticias/`, `/noticias/<slug>/`
- Funciones: Categorías, multimedia, SEO, relacionados

---

## 🔧 Archivos Clave

### Configuración
- `INGLAT/settings.py` - Configuración Django
- `requirements.txt` - Dependencias
- `.env` - Variables de entorno

### Apps Principales  
- `apps/core/` - Home y simulador solar
- `apps/projects/` - Portfolio
- `apps/blog/` - Noticias
- `apps/contact/` - Formularios y WhatsApp

---

## 🔄 Flujo de Desarrollo

### Antes de Cambios
1. Revisar `docs/Bug_tracking.md` para bugs conocidos
2. Consultar `docs/UI_UX_doc.md` para diseño
3. Verificar `docs/PRD.md` para requisitos

### Consideraciones
- **Seguridad**: Variables de entorno, no hardcodear credenciales
- **CSS/JS**: Archivos separados, no inline
- **Testing**: Responsive, formularios, AJAX endpoints

---

## 🎯 Estado del Proyecto

### ✅ Completado
- Setup Django + apps estructura
- Simulador solar con datos Argentina
- Sistema contacto + WhatsApp
- Blog con categorías

### ⏳ Pendiente  
- Dashboard clientes
- Deploy producción

---

**📞 Contacto**: +54 11 6721-4369 | info@inglat.com