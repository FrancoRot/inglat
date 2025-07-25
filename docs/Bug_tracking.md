# Bug_tracking.md - Seguimiento de Errores INGLAT

## Estado Actual
**Última actualización**: 25/07/2025  
**Bugs activos**: 0
**Bugs resueltos este mes**: 1  
**Total histórico**: 1

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

*No hay bugs activos actualmente*

---

## ✅ Bugs Resueltos Recientes (Últimos 10)

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