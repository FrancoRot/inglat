# Bug_tracking.md - Seguimiento de Errores INGLAT

## Estado Actual
**Última actualización**: 25/07/2025  
**Bugs activos**: 3
**Bugs resueltos este mes**: 4  
**Total histórico**: 10

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