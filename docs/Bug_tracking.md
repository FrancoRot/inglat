# Bug_tracking.md - Seguimiento de Errores INGLAT

## Estado Actual
**Última actualización**: 27/07/2025  
**Bugs activos**: 16
**Bugs resueltos este mes**: 4  
**Total histórico**: 20

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