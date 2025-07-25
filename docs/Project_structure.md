
## Stack Tecnológico

### Backend
- **Framework**: Django 4.2+ (LTS)
- **Lenguaje**: Python 3.11+
- **Base de Datos**: PostgreSQL
- **Cache**: Redis (opcional para producción)
- **Media Storage**: Django FileField + hostinger VPS (produccion)

### Frontend
- **Templates**: Django Templates + Jinja2
- **CSS**: CSS3 + Framework TBD (Bootstrap/Tailwind)
- **JavaScript**: Vanilla JS + Alpine.js para interactividad
- **Icons**: Font Awesome o Heroicons
- **Fonts**: Google Fonts

### DevOps & Tools
- **Versionado**: Git + GitHub
- **CI/CD**: GitHub Actions
- **Monitoring**: Django Debug Toolbar (dev)
- **Testing**: Django TestCase + Pytest

---

## Estructura de Directorios

```
inglat_project/
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── inglat/                     # Proyecto principal
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                       # Aplicaciones Django
│   ├── __init__.py
│   ├── core/                   # App principal
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── apps.py
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
│   │   ├── base.css
│   │   ├── components.css
│   │   └── pages.css
│   ├── js/
│   │   ├── main.js
│   │   ├── contact.js
│   │   └── utils.js
│   ├── images/
│   │   ├── logo/
│   │   ├── projects/
│   │   └── icons/
│   └── fonts/
├── media/                      # Archivos subidos
│   ├── projects/
│   ├── blog/
│   └── uploads/
├── docs/                       # Documentación
│   ├── PRD.md
│   ├── Project_structure.md
│   ├── Implementation.md
│   ├── UI_UX_doc.md
│   └── Bug_tracking.md
├── cursor/
│   └── rules/
│       ├── Generate.mdc
│       └── Workflow.mcd
├── CLAUDE.md
├── todo.md
└── README.md
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
Django>=4.2,<5.0
Pillow>=10.0.0
python-decouple>=3.6
django-environ>=0.9.0
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
- Crea archivos por página/app en `static/css/` y `static/js/` (ej: `static/css/about.css`, `static/js/contact.js`).
- No uses estilos ni scripts inline en los HTML.
- Referencia los archivos en los templates con `{% load static %}` y las etiquetas `<link>` y `<script>`.

### Ejemplo de referencia en un template:
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/about.css' %}">
<script src="{% static 'js/base.js' %}"></script>
<script src="{% static 'js/about.js' %}"></script>
```

- Comenta y etiqueta el código en español.
- Si cambias la estructura, actualiza esta documentación.

---