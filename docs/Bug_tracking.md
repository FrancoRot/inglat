# Bug_tracking.md - Seguimiento de Errores INGLAT

## Estado Actual
**Última actualización**: 13/08/2025  
**Bugs activos**: 3
**Bugs resueltos**: 28  
**Estado general**: ✅ ESTABLE

---

## Template para Reportar Bugs

### BUG-YYYY-MM-DD-XXX
**Fecha**: DD/MM/YYYY  
**Prioridad**: Crítica / Alta / Media / Baja  
**Estado**: Nuevo / En Progreso / Resuelto  
**Módulo**: Core / Projects / Blog / Contact  

**Descripción**: [Descripción clara del problema]
**Solución aplicada**: [Claude Code completa esto]
**Archivos modificados**: [Lista de archivos]

---

## 🔴 Bugs Activos (Solo Críticos/Altos)

### Bug #2 🔴 CRÍTICO
**DEBUG=True en producción**
- **Archivo**: `INGLAT/settings.py:26`
- **Solución**: `DEBUG = get_env_variable('DEBUG', 'False').lower() == 'true'`
- **Estado**: 🆕 Pendiente

### Bug #31 🟡 MEDIO  
**Elemento flotante indeseado en home**
- **Archivo**: `templates/base/header.html:49-63`
- **Causa**: Menú móvil visible en desktop
- **Estado**: 🔄 En investigación

### Bug #26 🟡 MEDIO
**Número WhatsApp hardcodeado**
- **Archivo**: `static/js/whatsapp.js:11`
- **Solución**: Verificar código país correcto (AR vs ES)
- **Estado**: 🆕 Pendiente

---

## ✅ Bugs Críticos Resueltos (Últimos 5)

1. **SECRET_KEY expuesta** → Variables entorno ✅
2. **Credenciales BD hardcodeadas** → .env implementado ✅  
3. **MEDIA_URL faltante** → Configurado ✅
4. **URLs projects rotas** → Corregidas ✅
5. **Slugs duplicados** → Generación única ✅

---

## 📚 Errores Comunes - Referencia

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

---

## ✅ Checklist Pre-Commit

- [ ] Sin errores de sintaxis
- [ ] Tests pasan  
- [ ] Sin `print()` olvidados
- [ ] Migraciones creadas
- [ ] Static files OK
- [ ] Variables de entorno actualizadas

---

## 📋 Gestión del Archivo

**Cuando llegues a 15 bugs resueltos:**
1. Archivar bugs antiguos de más de 1 mes
2. Mantener solo últimos 5 en "Resueltos Recientes"
3. Actualizar contador en "Estado Actual"

**Prioridades de documentación:**
- **Críticos/Altos**: Documentar completamente
- **Medios/Bajos**: Solo resumen básico