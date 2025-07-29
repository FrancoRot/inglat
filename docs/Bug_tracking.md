# Bug_tracking.md - Seguimiento de Errores INGLAT

## Estado Actual
**Última actualización**: 29/07/2025  
**Bugs activos**: 23
**Bugs resueltos este mes**: 7  
**Total histórico**: 30

---

## Template para Reportar Bugs

### BUG-YYYY-MM-DD-XXX
**Fecha**: DD/MM/YYYY  
**Prioridad**: Crítica / Alta / Media / Baja  
**Estado**: Nuevo / En Progreso / Resuelto  
**Módulo**: Core / Projects / Blog / Contact  

**Descripción**: [Descripción clara del problema]

**Pasos para reproducir**:
1. [Paso 1]
2. [Paso 2]  
3. [Resultado esperado vs obtenido]

**Solución aplicada**: [Claude Code completa esto]
**Archivos modificados**: [Claude Code completa esto]

---

## 🔴 Bugs Activos

## ✅ Bugs Resueltos Recientes (Últimos 10)

### Bug Report #1 ✅

### 📋 Información General
- **Fecha**: 2025-07-25 10:00:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 23
- **Tipo**: Seguridad
- **Severidad**: 🔴 Crítica
- **Estado**: ✅ Resuelto

### 🐛 Descripción del Problema
SECRET_KEY expuesta en el código fuente con valor por defecto inseguro

### ✅ Solución Aplicada
```python
SECRET_KEY = get_env_variable('SECRET_KEY', 'django-insecure-d60r9p8sk!d#7=f%8_7^l*a21$*n@s8rjk&kepfr0+ve8r%9j9')
```

**Archivos modificados**: `INGLAT/settings.py`
**Fecha resolución**: 2025-07-25

---

## Bug Report #2

### 📋 Información General
- **Fecha**: 2025-07-25 10:05:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 26
- **Tipo**: Seguridad
- **Severidad**: 🔴 Crítica
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
DEBUG=True habilitado en settings, vulnerable para producción

### 💻 Código Problemático
```python
DEBUG = True
```

### ✅ Solución Recomendada
```python
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
```

---

### Bug Report #3 ✅

### 📋 Información General
- **Fecha**: 2025-07-25 10:10:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 84
- **Tipo**: Seguridad
- **Severidad**: 🔴 Crítica
- **Estado**: ✅ Resuelto

### 🐛 Descripción del Problema
Credenciales de base de datos expuestas en código fuente

### ✅ Solución Aplicada
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('DB_NAME', 'inglat_db'),
        'USER': get_env_variable('DB_USER', 'postgres'),
        'PASSWORD': get_env_variable('DB_PASSWORD', 'franco4369'),
        'HOST': get_env_variable('DB_HOST', 'localhost'),
        'PORT': get_env_variable('DB_PORT', '5432'),
    }
}
```

**Archivos modificados**: `INGLAT/settings.py`
**Fecha resolución**: 2025-07-25

---

### Bug Report #4 ✅

### 📋 Información General
- **Fecha**: 2025-07-25 10:15:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 28
- **Tipo**: Seguridad
- **Severidad**: 🟠 Alta
- **Estado**: ✅ Resuelto

### 🐛 Descripción del Problema
ALLOWED_HOSTS vacío, puede causar problemas de seguridad en producción

### ✅ Solución Aplicada
```python
ALLOWED_HOSTS = get_env_variable('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

**Archivos modificados**: `INGLAT/settings.py`
**Fecha resolución**: 2025-07-25

---

## 🔴 Bugs Activos

## 🔴 CRÍTICA - Atención Inmediata

## Bug Report #7

### 📋 Información General
- **Fecha**: 2025-07-27 16:00:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 37
- **Tipo**: Seguridad
- **Severidad**: 🔴 Crítica
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
DEBUG=True habilitado en producción - vulnerabilidad crítica de seguridad

### 💻 Código Problemático
```python
DEBUG = True
```

### ✅ Solución Recomendada
```python
DEBUG = get_env_variable('DEBUG', 'False').lower() in ['true', '1', 'yes']
```

---

## Bug Report #8

### 📋 Información General
- **Fecha**: 2025-07-27 16:05:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 95
- **Tipo**: Seguridad
- **Severidad**: 🔴 Crítica
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Credenciales de base de datos expuestas en código fuente (PASSWORD visible)

### 💻 Código Problemático
```python
'PASSWORD': get_env_variable('DB_PASSWORD', 'franco4369'),
```

### ✅ Solución Recomendada
```python
'PASSWORD': get_env_variable('DB_PASSWORD'),  # Sin valor por defecto
```

---

## Bug Report #9

### 📋 Información General
- **Fecha**: 2025-07-27 16:10:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 34
- **Tipo**: Seguridad
- **Severidad**: 🔴 Crítica
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
SECRET_KEY con valor por defecto inseguro expuesto en código

### 💻 Código Problemático
```python
SECRET_KEY = get_env_variable('SECRET_KEY', 'django-insecure-d60r9p8sk!d#7=f%8_7^l*a21$*n@s8rjk&kepfr0+ve8r%9j9')
```

### ✅ Solución Recomendada
```python
SECRET_KEY = get_env_variable('SECRET_KEY')  # Sin valor por defecto
```

---

## 🟠 ALTA PRIORIDAD

## Bug Report #10

### 📋 Información General
- **Fecha**: 2025-07-27 16:15:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 124-130
- **Tipo**: Configuración
- **Severidad**: 🟠 Alta
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Configuración de internacionalización incorrecta - idioma en inglés para sitio en español

### 💻 Código Problemático
```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
```

### ✅ Solución Recomendada
```python
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'  # o 'America/Argentina/Buenos_Aires'
```

---

## Bug Report #21

### 📋 Información General
- **Fecha**: 2025-07-29 10:00:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 144
- **Tipo**: Configuración
- **Severidad**: 🟠 Alta
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
MEDIA_URL y MEDIA_ROOT no definidos para ImageField de Project model

### 💻 Código Problemático
```python
# MEDIA settings missing but ImageField in Project model requires them
```

### ✅ Solución Recomendada
```python
# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## Bug Report #13

### 📋 Información General
- **Fecha**: 2025-07-27 16:30:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/models.py`
- **Línea**: 102-104
- **Tipo**: Bug
- **Severidad**: 🟠 Alta
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
get_absolute_url referencia URL inexistente 'core:project_detail'

### 💻 Código Problemático
```python
def get_absolute_url(self):
    return reverse('core:project_detail', kwargs={'slug': self.slug})
```

### ✅ Solución Recomendada
```python
def get_absolute_url(self):
    return reverse('projects:detail', kwargs={'slug': self.slug})
```

---

## Bug Report #23

### 📋 Información General
- **Fecha**: 2025-07-29 10:10:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/models.py`
- **Línea**: 99-100
- **Tipo**: Bug
- **Severidad**: 🟠 Alta
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Potencial bug de slug duplicado - no maneja unicidad automática

### 💻 Código Problemático
```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kwargs)
```

### ✅ Solución Recomendada
```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = self._generate_unique_slug()
    super().save(*args, **kwargs)

def _generate_unique_slug(self):
    slug = slugify(self.title)
    unique_slug = slug
    counter = 1
    while Project.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    return unique_slug
```

---

## Bug Report #25

### 📋 Información General
- **Fecha**: 2025-07-29 10:20:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/views.py`
- **Línea**: 104
- **Tipo**: Seguridad
- **Severidad**: 🟠 Alta
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Conversión de datos de entrada sin validación puede causar errores o vulnerabilidades

### 💻 Código Problemático
```python
consumo_anual = float(data.get('consumo_anual', 0))
superficie = float(data.get('superficie', 0))
```

### ✅ Solución Recomendada
```python
try:
    consumo_anual = float(data.get('consumo_anual', 0))
    if consumo_anual < 0 or consumo_anual > 50000:
        raise ValueError("Consumo anual fuera de rango válido")
except (ValueError, TypeError):
    return JsonResponse({'success': False, 'error': 'Consumo anual inválido'}, status=400)
```

---

## 🟡 MEDIA PRIORIDAD

---

## Bug Report #24

### 📋 Información General
- **Fecha**: 2025-07-29 10:15:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/views.py`
- **Línea**: 36-53
- **Tipo**: Redundancia
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Código duplicado entre HomeView (CBV) e index (FBV) - violación principio DRY

### 💻 Código Problemático
```python
# Misma lógica duplicada en ambas vistas
featured_projects = Project.objects.filter(is_featured=True, is_active=True)
```

### ✅ Solución Recomendada
```python
# Eliminar una de las dos vistas y usar solo HomeView (CBV preferido)
# O extraer lógica común en un método helper
```

---

## Bug Report #25

### 📋 Información General
- **Fecha**: 2025-07-29 10:20:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/views.py`
- **Línea**: 104
- **Tipo**: Seguridad
- **Severidad**: 🟠 Alta
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Conversión de datos de entrada sin validación puede causar errores o vulnerabilidades

### 💻 Código Problemático
```python
consumo_anual = float(data.get('consumo_anual', 0))
superficie = float(data.get('superficie', 0))
```

### ✅ Solución Recomendada
```python
try:
    consumo_anual = float(data.get('consumo_anual', 0))
    if consumo_anual < 0 or consumo_anual > 50000:
        raise ValueError("Consumo anual fuera de rango válido")
except (ValueError, TypeError):
    return JsonResponse({'success': False, 'error': 'Consumo anual inválido'}, status=400)
```

---

## Bug Report #26

### 📋 Información General
- **Fecha**: 2025-07-29 10:25:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/static/js/whatsapp.js`
- **Línea**: 11
- **Tipo**: Configuración
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Número de teléfono hardcodeado en JavaScript con código de Argentina pero empresa parece estar en España

### 💻 Código Problemático
```javascript
phoneNumber: '541167214369',
```

### ✅ Solución Recomendada
```javascript
// Verificar ubicación real de la empresa y usar código correcto
phoneNumber: '34912345678', // Si está en España
// O mantener Argentina si es correcto
```

---

## Bug Report #27

### 📋 Información General
- **Fecha**: 2025-07-29 10:30:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/blog/models.py`
- **Línea**: 1
- **Tipo**: Arquitectura
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Modelo de blog vacío pero app está registrada en INSTALLED_APPS

### 💻 Código Problemático
```python
# Archivo completamente vacío
```

### ✅ Solución Recomendada
```python
# Implementar modelos básicos de blog o remover de INSTALLED_APPS
from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    # ... resto del modelo
```

---

## Bug Report #28

### 📋 Información General
- **Fecha**: 2025-07-29 10:35:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/contact/models.py`
- **Línea**: 1
- **Tipo**: Arquitectura
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Modelo de contacto vacío pero app está registrada en INSTALLED_APPS

### 💻 Código Problemático
```python
# Archivo completamente vacío
```

### ✅ Solución Recomendada
```python
# Implementar modelo de contacto o remover de INSTALLED_APPS
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    # ... resto del modelo
```

---

## Bug Report #29

### 📋 Información General
- **Fecha**: 2025-07-29 10:40:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/requirements.txt`
- **Línea**: 1-9
- **Tipo**: Dependencias
- **Severidad**: 🟢 Baja
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
python-decouple instalado pero no utilizado en settings.py

### 💻 Código Problemático
```python
# En requirements.txt: python-decouple==3.8
# Pero en settings.py se usa os.environ directamente
```

### ✅ Solución Recomendada
```python
# Usar python-decouple para mejor manejo de variables de entorno
from decouple import config
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

---

## Bug Report #30

### 📋 Información General
- **Fecha**: 2025-07-29 10:45:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/templates/base/base.html`
- **Línea**: 20, 31-34
- **Tipo**: Recursos
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Referencias a imágenes que probablemente no existen (favicon, og-image, etc.)

### 💻 Código Problemático
```html
<meta property="og:image" content="{% static 'images/og-image.jpg' %}">
<link rel="icon" type="image/x-icon" href="{% static 'images/favicon.ico' %}">
```

### ✅ Solución Recomendada
```python
# Crear las imágenes referenciadas o usar placeholders
# Verificar que existan en static/images/
```

---

## Bug Report #7

### 📋 Información General
- **Fecha**: 2025-07-27 16:00:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 37
- **Tipo**: Seguridad
- **Severidad**: 🔴 Crítica
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
DEBUG=True habilitado en producción - vulnerabilidad crítica de seguridad

### 💻 Código Problemático
```python
DEBUG = True
```

### ✅ Solución Recomendada
```python
DEBUG = get_env_variable('DEBUG', 'False').lower() in ['true', '1', 'yes']
```

---

## Bug Report #8

### 📋 Información General
- **Fecha**: 2025-07-27 16:05:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 95
- **Tipo**: Seguridad
- **Severidad**: 🔴 Crítica
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Credenciales de base de datos expuestas en código fuente (PASSWORD visible)

### 💻 Código Problemático
```python
'PASSWORD': get_env_variable('DB_PASSWORD', 'franco4369'),
```

### ✅ Solución Recomendada
```python
'PASSWORD': get_env_variable('DB_PASSWORD'),  # Sin valor por defecto
```

---

## Bug Report #9

### 📋 Información General
- **Fecha**: 2025-07-27 16:10:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 34
- **Tipo**: Seguridad
- **Severidad**: 🔴 Crítica
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
SECRET_KEY con valor por defecto inseguro expuesto en código

### 💻 Código Problemático
```python
SECRET_KEY = get_env_variable('SECRET_KEY', 'django-insecure-d60r9p8sk!d#7=f%8_7^l*a21$*n@s8rjk&kepfr0+ve8r%9j9')
```

### ✅ Solución Recomendada
```python
SECRET_KEY = get_env_variable('SECRET_KEY')  # Sin valor por defecto
```

---

## Bug Report #10

### 📋 Información General
- **Fecha**: 2025-07-27 16:15:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 124-130
- **Tipo**: Configuración
- **Severidad**: 🟠 Alta
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Configuración de internacionalización incorrecta - idioma en inglés para sitio en español

### 💻 Código Problemático
```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
```

### ✅ Solución Recomendada
```python
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'  # o 'America/Argentina/Buenos_Aires'
```

---

## Bug Report #11

### 📋 Información General
- **Fecha**: 2025-07-27 16:20:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/settings.py`
- **Línea**: 136-144
- **Tipo**: Configuración
- **Severidad**: 🟠 Alta
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
MEDIA_URL y MEDIA_ROOT no definidos pero necesarios para ImageField

### 💻 Código Problemático
```python
# MEDIA settings missing
```

### ✅ Solución Recomendada
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Add to urls.py if DEBUG:
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Bug Report #12

### 📋 Información General
- **Fecha**: 2025-07-27 16:25:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/views.py`
- **Línea**: 32-49
- **Tipo**: Rendimiento
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Código duplicado entre HomeView y función index - violación DRY

### 💻 Código Problemático
```python
# Misma consulta y contexto duplicado en ambas vistas
featured_projects = Project.objects.filter(...)
```

### ✅ Solución Recomendada
```python
# Usar solo una vista (CBV preferido) o extraer lógica común
class HomeView(TemplateView):
    # Mantener solo esta vista
```

---

## Bug Report #13

### 📋 Información General
- **Fecha**: 2025-07-27 16:30:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/models.py`
- **Línea**: 102-104
- **Tipo**: Bug
- **Severidad**: 🟠 Alta
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
get_absolute_url referencia URL inexistente 'core:project_detail'

### 💻 Código Problemático
```python
def get_absolute_url(self):
    return reverse('core:project_detail', kwargs={'slug': self.slug})
```

### ✅ Solución Recomendada
```python
def get_absolute_url(self):
    return reverse('projects:detail', kwargs={'slug': self.slug})
```

---

## Bug Report #14

### 📋 Información General
- **Fecha**: 2025-07-27 16:35:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/models.py`
- **Línea**: 96-100
- **Tipo**: Bug
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Potencial conflicto de slugs - no maneja duplicados al generar slug

### 💻 Código Problemático
```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kwargs)
```

### ✅ Solución Recomendada
```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = self._generate_unique_slug()
    super().save(*args, **kwargs)

def _generate_unique_slug(self):
    slug = slugify(self.title)
    unique_slug = slug
    counter = 1
    while Project.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    return unique_slug
```

---

## Bug Report #15

### 📋 Información General
- **Fecha**: 2025-07-27 16:40:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/admin.py`
- **Línea**: 80-84
- **Tipo**: Rendimiento
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
CSS y JS referencias en admin pueden no existir, causando errores 404

### 💻 Código Problemático
```python
class Media:
    css = {
        'all': ('admin/css/custom-project-admin.css',)
    }
    js = ('admin/js/custom-project-admin.js',)
```

### ✅ Solución Recomendada
```python
# Verificar que los archivos existan o remover la clase Media
# class Media:
#     css = {'all': ('admin/css/custom-project-admin.css',)}
#     js = ('admin/js/custom-project-admin.js',)
```

---

## Bug Report #16

### 📋 Información General
- **Fecha**: 2025-07-27 16:45:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/templates/core/home.html`
- **Línea**: 223
- **Tipo**: Usabilidad
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Número de teléfono falso/placeholder en enlace de llamada

### 💻 Código Problemático
```html
<a href="tel:+34XXX-XXX-XXX" class="btn btn--secondary">
```

### ✅ Solución Recomendada
```html
<a href="tel:+34912345678" class="btn btn--secondary">
```

---

## Bug Report #17

### 📋 Información General
- **Fecha**: 2025-07-27 16:50:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/templates/base/base.html`
- **Línea**: 112
- **Tipo**: Usabilidad
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
URL de WhatsApp incorrecta (código Argentina en lugar de España)

### 💻 Código Problemático
```html
<a href="https://wa.me/54XXXXXXXXX?text=..."
```

### ✅ Solución Recomendada
```html
<a href="https://wa.me/34912345678?text=..."
```

---

## Bug Report #18

### 📋 Información General
- **Fecha**: 2025-07-27 16:55:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/static/js/home.js`
- **Línea**: 388-408
- **Tipo**: Rendimiento
- **Severidad**: 🟢 Baja
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Monitoreo de performance solo en localhost - debería estar en modo desarrollo

### 💻 Código Problemático
```javascript
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
```

### ✅ Solución Recomendada
```javascript
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.INGLAT?.debug) {
```

---

## Bug Report #19

### 📋 Información General
- **Fecha**: 2025-07-27 17:00:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/urls.py`
- **Línea**: 7
- **Tipo**: Codificación
- **Severidad**: 🟢 Baja
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Caracteres mal codificados en comentarios

### 💻 Código Problemático
```python
# P�gina de inicio - usando vista funci�n
```

### ✅ Solución Recomendada
```python
# Página de inicio - usando vista función
```

---

## Bug Report #20

### 📋 Información General
- **Fecha**: 2025-07-27 17:05:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/static/css/home.css`
- **Línea**: 425-436
- **Tipo**: Accesibilidad
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Uso de font-size: 0 en botones puede causar problemas de accesibilidad

### 💻 Código Problemático
```css
.project-card__toggle-text {
    font-size: 0;
}
```

### ✅ Solución Recomendada
```css
.project-card__toggle-text {
    position: absolute;
    left: -9999px;
    width: 1px;
    height: 1px;
    overflow: hidden;
}
```

---

## Bug Report #5

### 📋 Información General
- **Fecha**: 2025-07-25 10:20:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/INGLAT/urls.py`
- **Línea**: 37
- **Tipo**: Práctica
- **Severidad**: 🟡 Media
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
MEDIA_URL comentado pero no definido en settings.py

### 💻 Código Problemático
```python
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### ✅ Solución Recomendada
Agregar en settings.py:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## Bug Report #6

### 📋 Información General
- **Fecha**: 2025-07-25 10:25:00
- **Archivo**: `/mnt/c/Users/franc/Desktop/INGLAT/codigo/apps/core/urls.py`
- **Línea**: 7
- **Tipo**: Práctica
- **Severidad**: 🟢 Baja
- **Estado**: 🆕 Nuevo

### 🐛 Descripción del Problema
Caracteres especiales mal codificados en comentarios

### 💻 Código Problemático
```python
# P�gina de inicio - usando vista funci�n
```

### ✅ Solución Recomendada
```python
# Página de inicio - usando vista función
```

---

### BUG-2025-07-25-01 ✅
**Fecha**: 25/07/2025  
**Prioridad**: Baja  
**Estado**: Resuelto  
**Módulo**: Core  

**Descripción**: no renderiza la pagina de home

**Pasos para reproducir**:
1. ingreso a home y no veo la pagina

**Solución aplicada**: Resuelto el 25/07/2025
**Archivos modificados**: N/A

---

## 📚 Errores Comunes - Referencia Permanente

### Django Import Errors
**Síntoma**: `ModuleNotFoundError`  
**Solución**: Verificar INSTALLED_APPS

### Template Not Found
**Síntoma**: `TemplateDoesNotExist`  
**Solución**: Verificar TEMPLATES['DIRS']

### Static Files Issues  
**Síntoma**: CSS/JS no carga  
**Solución**: `python manage.py collectstatic`

### CSRF Token Missing
**Síntoma**: `Forbidden (403)`  
**Solución**: Agregar `{% csrf_token %}`

### Migration Conflicts
**Síntoma**: `InconsistentMigrationHistory`  
**Solución**: `python manage.py migrate`

---

## 🛠️ Debugging Quick Tips

```python
# Ver logs
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug info")

# Debug temporal
print(f"Variable: {mi_variable}")

# Verificar queries
from django.db import connection
print(f"Queries: {len(connection.queries)}")
```

---

## ✅ Checklist Pre-Commit

- [ ] Sin errores de sintaxis
- [ ] Tests pasan  
- [ ] Sin `print()` olvidados
- [ ] Migraciones creadas
- [ ] Static files OK

---

## 📋 Gestión del Archivo

**Cuando llegues a 15 bugs resueltos:**
1. Borrar bugs antiguos de mas de 1 mes
2. Mantener solo últimos 10 en "Resueltos Recientes"
3. Actualizar contador en "Estado Actual"

**Prioridades de documentación:**
- **Críticos/Altos**: Siempre documentar completamente
- **Medios**: Documentar solución básica
- **Bajos**: Solo contador estadístico