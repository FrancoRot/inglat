# 📰 EstefaniPUBLI - Guía Completa de Uso

## 🎯 **Resumen del Sistema**

EstefaniPUBLI es un agente inteligente que **investiga**, **reformula** y **publica** noticias de energías renovables automáticamente, con contenido visual HTML rico y 5 plantillas diferentes para evitar contenido mecánico.

---

## 🛠️ **Comandos Disponibles**

### 1. **🔍 Investigación** - `estefani_investigar`
Genera noticias candidatas en formato JSON.

```bash
# Básico - 5 noticias variadas
python manage.py estefani_investigar

# Personalizado - cantidad específica
python manage.py estefani_investigar --max-noticias=10 --modo=exhaustivo

# Solo portales argentinos  
python manage.py estefani_investigar --portales=argentina_only --max-noticias=8

# Modo rápido - 3 noticias
python manage.py estefani_investigar --modo=rapido
```

### 2. **📋 Publicación Selectiva** - `estefani_publicar_selectivo` 
Permite elegir qué noticias publicar del JSON generado.

```bash
# Ver candidatos disponibles SIN publicar
python manage.py estefani_publicar_selectivo --listar

# Publicar noticias específicas por número
python manage.py estefani_publicar_selectivo --indices=1,3,5

# Publicar por rango
python manage.py estefani_publicar_selectivo --indices=1-3

# Publicar por categoría
python manage.py estefani_publicar_selectivo --categoria="Energía Solar"

# Publicar por palabra en título
python manage.py estefani_publicar_selectivo --titulo-contiene="argentina"

# 🎯 CREAR COMO BORRADORES (recomendado)
python manage.py estefani_publicar_selectivo --indices=1,2,4 --draft-mode

# Sin descargar imágenes
python manage.py estefani_publicar_selectivo --indices=1,2 --skip-images
```

### 3. **🧹 Limpieza** - `estefani_limpiar`
Gestiona noticias no deseadas.

```bash
# Listar noticias inactivas sin eliminar
python manage.py estefani_limpiar --inactivas --listar

# Eliminar solo noticias inactivas (borradores)
python manage.py estefani_limpiar --inactivas

# Eliminar noticias específicas por ID
python manage.py estefani_limpiar --por-ids=20,21,22

# Eliminar por rango de IDs
python manage.py estefani_limpiar --por-ids=20-25

# Eliminar noticias más antiguas que X días
python manage.py estefani_limpiar --antiguas=7

# 🚨 ELIMINAR TODAS las noticias de Estefani
python manage.py estefani_limpiar --todas-estefani --confirmar
```

### 4. **🚀 Publicación Masiva** - `estefani_publicar`
Publica todas las noticias del JSON de una vez.

```bash
# Publicar todas como borradores
python manage.py estefani_publicar --draft-mode

# Simular publicación sin crear registros
python manage.py estefani_publicar --dry-run

# Publicar todas activas (no recomendado)
python manage.py estefani_publicar
```

---

## 🎯 **Flujo de Trabajo Recomendado**

### **Paso 1: Generar Candidatos** 🔍
```bash
python manage.py estefani_investigar --max-noticias=8 --modo=exhaustivo
```
- Genera 8 noticias candidatas con contenido HTML rico
- Cada noticia usa plantilla visual diferente (no mecánico)
- Se guarda en `shared_memory/noticias_estefani.json`

### **Paso 2: Revisar Candidatos** 📋
```bash
python manage.py estefani_publicar_selectivo --listar
```
- Muestra todas las noticias disponibles numeradas
- Puedes ver títulos y categorías antes de decidir

### **Paso 3: Publicar Como Borradores** 📝
```bash
python manage.py estefani_publicar_selectivo --indices=1,3,5,7 --draft-mode
```
- Selecciona las noticias que más te gusten
- Se crean como **inactivas** (borradores)
- No aparecen en el sitio web aún

### **Paso 4: Revisar en Django Admin** 🎨
```bash
# Ir a: http://localhost:8000/admin/blog/noticia/
```
- Revisa el contenido HTML con formato visual
- Edita lo que necesites
- **Marca como `activa=True`** las que quieres publicar
- Las demás las puedes dejar como borradores

### **Paso 5: Limpiar Borradores No Usados** 🧹
```bash
python manage.py estefani_limpiar --inactivas --listar  # Ver qué hay
python manage.py estefani_limpiar --inactivas           # Eliminar borradores
```

---

## ✨ **Características del Sistema**

### **📝 Contenido Inteligente**
- **5 plantillas diferentes**: Análisis de Mercado, Oportunidades, Tendencias, Casos de Éxito, Innovación
- **Rotación aleatoria**: Cada noticia usa formato visual diferente
- **HTML rico**: Colores, gradientes, cajas destacadas, grids responsivos
- **SEO optimizado**: Meta tags automáticos para Google

### **🖼️ Gestión de Imágenes**
- Extracción automática desde URLs originales
- Validación robusta de formatos y tamaños  
- Fallbacks inteligentes cuando no hay imágenes
- Descarga con retry y manejo de errores

### **🏷️ Categorización Automática**
- Asignación inteligente según contenido
- Creación automática de categorías faltantes
- Fallbacks a categorías existentes

### **🎛️ Control Total**
- **Borradores primero**: Revisar antes de publicar
- **Selección granular**: Elegir exactamente qué publicar
- **Limpieza fácil**: Eliminar lo no deseado
- **Sin duplicados**: Detección automática de títulos similares

---

## 📊 **Estado de Noticias**

### **Ver Estado Actual**
```bash
# Via Django shell
python manage.py shell -c "
from apps.blog.models import Noticia
noticias = Noticia.objects.filter(autor='Estefani')
print(f'Total: {noticias.count()}')
print(f'Activas: {noticias.filter(activa=True).count()}')
print(f'Borradores: {noticias.filter(activa=False).count()}')
"
```

### **Acceso al Admin**
- **URL**: `http://localhost:8000/admin/blog/noticia/`
- **Filtrar por autor**: "Estefani" en el filtro lateral
- **Estados**: Activa ✅ | Inactiva ❌

---

## 🚨 **Casos de Uso Comunes**

### **Generar 10 noticias, publicar 3 mejores**
```bash
python manage.py estefani_investigar --max-noticias=10
python manage.py estefani_publicar_selectivo --listar
python manage.py estefani_publicar_selectivo --indices=2,5,8 --draft-mode
# Revisar en admin y activar manualmente
```

### **Limpiar todo y empezar de cero**
```bash
python manage.py estefani_limpiar --todas-estefani
python manage.py estefani_investigar --max-noticias=5
python manage.py estefani_publicar_selectivo --indices=1-3 --draft-mode
```

### **Solo noticias sobre Argentina**
```bash
python manage.py estefani_investigar --portales=argentina_only
python manage.py estefani_publicar_selectivo --titulo-contiene="argentina" --draft-mode
```

### **Eliminar borradores viejos**
```bash
python manage.py estefani_limpiar --inactivas --antiguas=7
```

---

## 🎨 **Ejemplos de Plantillas**

El sistema genera automáticamente contenido como:

1. **📊 Análisis de Mercado**: Headers con gradientes, cajas informativas
2. **🚀 Oportunidades**: Grids de beneficios, call-to-actions
3. **🔮 Tendencias**: Timeline headers, factores clave con tags
4. **✅ Casos de Éxito**: Banners de éxito, cards de beneficios  
5. **🔬 Innovación**: Headers tech, grids técnicos, quotes destacadas

**Resultado**: Cada noticia tiene formato visual único y atractivo 🎨

---

## 🏃‍♂️ **Inicio Rápido**

```bash
# 1. Generar noticias
python manage.py estefani_investigar

# 2. Ver candidatos  
python manage.py estefani_publicar_selectivo --listar

# 3. Publicar las mejores como borradores
python manage.py estefani_publicar_selectivo --indices=1,3,5 --draft-mode

# 4. Ir al admin y activar las que quieras
# http://localhost:8000/admin/blog/noticia/

# 5. Limpiar borradores no usados
python manage.py estefani_limpiar --inactivas
```

¡**EstefaniPUBLI está lista para generar contenido de calidad para INGLAT!** 🚀