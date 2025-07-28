# Integración de WhatsApp - INGLAT

## Resumen

Este documento describe la implementación del botón flotante de WhatsApp en la aplicación INGLAT, incluyendo configuración, personalización y mantenimiento.

## Características Implementadas

### ✅ Funcionalidades Principales

- **Botón flotante fijo** en esquina inferior derecha
- **Detección inteligente de dispositivo** (móvil vs escritorio)
- **Apertura automática** de WhatsApp app en móviles
- **Apertura de WhatsApp Web** en navegadores de escritorio
- **Mensaje predeterminado** personalizable
- **Diseño responsive** y accesible
- **Animaciones y efectos hover** profesionales
- **Analytics y tracking** opcional

### 📱 Comportamiento por Dispositivo

| Dispositivo | Comportamiento | URL Utilizada |
|------------|----------------|---------------|
| **Móvil Android** | Abre WhatsApp app directamente | `whatsapp://send?phone=...` |
| **Móvil iOS** | Abre WhatsApp app directamente | `whatsapp://send?phone=...` |
| **Desktop** | Abre WhatsApp Web en nueva pestaña | `https://web.whatsapp.com/send?phone=...` |
| **Fallback** | Usa wa.me universal | `https://wa.me/...` |

## Configuración Actual

### 📞 Datos de Contacto

```javascript
const config = {
    phoneNumber: '541167214369',
    defaultMessage: 'Hola, me interesa obtener más información sobre sus servicios.',
    fallbackUrl: 'https://wa.me/541167214369'
};
```

### 🎨 Diseño Visual

- **Color principal**: #25D366 (verde oficial WhatsApp)
- **Color hover**: #20BA5A
- **Tamaño**: 60px × 60px
- **Posición**: Fijo, bottom: 24px, right: 24px
- **Z-index**: 1000 (siempre visible)
- **Animación**: Efecto pulso cada 2 segundos

## Archivos Involucrados

### 📁 Estructura de Archivos

```
INGLAT/
├── templates/base/base.html        # Botón HTML y configuración
├── static/css/base.css             # Estilos base del botón (.whatsapp-float)
├── static/css/whatsapp-fix.css     # Estilos específicos con !important para evitar conflictos
├── static/js/whatsapp.js           # Lógica inteligente de apertura
└── docs/WhatsApp_Integration.md    # Esta documentación
```

### 🔧 Archivos Modificados

1. **templates/base/base.html**
   - Botón flotante con número correcto
   - Schema.org actualizado con datos argentinos
   - Script de WhatsApp incluido

2. **static/css/base.css**
   - Estilos completos del botón flotante
   - Animaciones y efectos hover
   - Responsive design

3. **static/js/whatsapp.js** (NUEVO)
   - Detección inteligente de dispositivos
   - Lógica de apertura por plataforma
   - Analytics y tracking
   - Manejo de errores

4. **static/css/whatsapp-fix.css** (NUEVO)
   - Estilos específicos con !important
   - Corrección de tamaño y posición
   - Prevención de conflictos CSS
   - Responsive design optimizado

## Personalización

### 📱 Cambiar Número de Teléfono

**Opción 1: En JavaScript (Recomendado)**
```javascript
// Editar en static/js/whatsapp.js
const config = {
    phoneNumber: 'TU_NUEVO_NUMERO',  // Formato: 541167214369
    // ...
};
```

**Opción 2: En HTML (Fallback)**
```html
<!-- Editar en templates/base/base.html -->
<a href="https://wa.me/TU_NUEVO_NUMERO?text=..." 
   class="whatsapp-float" 
   id="whatsapp-button">
```

### 💬 Personalizar Mensaje

```javascript
// Editar en static/js/whatsapp.js
const config = {
    defaultMessage: 'Tu nuevo mensaje personalizado aquí',
    // ...
};
```

### 🎨 Cambiar Colores

```css
/* Editar en static/css/base.css */
.whatsapp-float {
    background: #TU_COLOR;  /* Color principal */
}

.whatsapp-float:hover {
    background: #TU_COLOR_HOVER;  /* Color al hacer hover */
}
```

### 📍 Cambiar Posición

```css
/* Editar en static/css/base.css */
.whatsapp-float {
    bottom: var(--space-X);  /* Cambiar distancia desde abajo */
    right: var(--space-X);   /* Cambiar distancia desde derecha */
    /* También puedes usar: left: var(--space-X); para esquina izquierda */
}
```

## Testing y Validación

### ✅ Checklist de Pruebas

#### Funcionalidad
- [ ] Botón aparece en todas las páginas
- [ ] Click abre WhatsApp correctamente en móviles
- [ ] Click abre WhatsApp Web en desktop
- [ ] Mensaje predeterminado se incluye correctamente
- [ ] Número de teléfono es correcto

#### Diseño
- [ ] Botón responsive en móviles (320px - 768px)
- [ ] Botón responsive en tablets (768px - 1024px)
- [ ] Botón responsive en desktop (1024px+)
- [ ] Efectos hover funcionan en desktop
- [ ] Animación de pulso activa
- [ ] No interfiere con otros elementos

#### Técnico
- [ ] No hay errores en consola del navegador
- [ ] Script se carga correctamente
- [ ] Funciona sin JavaScript (fallback HTML)
- [ ] Accesibilidad (aria-label, screen readers)

### 🔧 Herramientas de Testing

```javascript
// En modo desarrollo, abrir consola y ejecutar:
window.WhatsAppDebug.DeviceDetector.getDeviceInfo()

// Para probar URLs:
window.WhatsAppDebug.URLBuilder.buildWhatsAppUrl(true)  // Móvil
window.WhatsAppDebug.URLBuilder.buildWhatsAppUrl(false) // Desktop
```

### 📱 Testing en Dispositivos

#### Simulación en Chrome DevTools
1. Abrir DevTools (F12)
2. Activar "Toggle device toolbar" (Ctrl+Shift+M)
3. Seleccionar dispositivo móvil
4. Refrescar página y probar botón

#### Dispositivos Reales
- **Android**: Debe abrir app WhatsApp directamente
- **iPhone**: Debe abrir app WhatsApp directamente
- **Desktop**: Debe abrir WhatsApp Web en nueva pestaña

## Troubleshooting

### ⚠️ Problemas Comunes

#### 1. Botón no aparece
```bash
# Verificar que los archivos estáticos se cargan
python manage.py collectstatic

# Verificar en navegador -> F12 -> Network
# Buscar: whatsapp.js y base.css
```

#### 2. No abre WhatsApp en móvil
```javascript
// Verificar configuración en whatsapp.js
console.log(window.WhatsAppDebug.config.phoneNumber);
// Debe mostrar: "541167214369"
```

#### 3. Mensaje no aparece
```javascript
// Verificar codificación URL
console.log(window.WhatsAppDebug.URLBuilder.formatMessage('Tu mensaje'));
```

#### 4. Estilos no se aplican
```css
/* Verificar que base.css se carga y contiene: */
.whatsapp-float {
    position: fixed;
    /* ... resto de estilos */
}
```

### 🚨 Errores Típicos y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| Botón sin estilos | CSS no cargado | Verificar `{% load static %}` |
| No abre en móvil | Número incorrecto | Verificar formato internacional |
| JavaScript no funciona | Script no incluido | Verificar inclusión en base.html |
| Mensaje con caracteres extraños | Codificación URL incorrecta | Usar `encodeURIComponent()` |

## Analytics y Monitoreo

### 📊 Tracking Implementado

El sistema incluye tracking automático de:
- Clicks en el botón
- Tipo de dispositivo usado
- Método de apertura (app/web/fallback)
- Errores en apertura

### 🔍 Configurar Google Analytics

```javascript
// Si tienes Google Analytics instalado, automáticamente se trackeará:
// Evento: 'whatsapp_click'
// Categoría: 'contact'
// Label: 'click', 'error', etc.
```

### 📈 Métricas Recomendadas

- **CTR del botón**: Clicks / Visualizaciones de página
- **Conversión por dispositivo**: Móvil vs Desktop
- **Errores de apertura**: Fallos en abrir WhatsApp
- **Tiempo de respuesta**: Velocidad de apertura

## Mantenimiento

### 🔄 Actualizaciones Recomendadas

#### Mensual
- [ ] Verificar que el número de teléfono sigue activo
- [ ] Probar funcionalidad en diferentes dispositivos
- [ ] Revisar analytics de uso

#### Trimestral
- [ ] Actualizar mensaje estacional si aplica
- [ ] Revisar compatibilidad con nuevos navegadores
- [ ] Optimizar rendimiento si es necesario

#### Anual
- [ ] Revisar y actualizar documentación
- [ ] Evaluar nuevas funcionalidades de WhatsApp Business API
- [ ] Considerar A/B testing de diferentes mensajes

### 📝 Registro de Cambios

| Fecha | Versión | Cambios |
|-------|---------|---------|
| 2024-01 | 1.0 | Implementación inicial |
| 2024-XX | 1.1 | Número y mensaje actualizados |

---

## Soporte

Para soporte técnico o modificaciones:

1. **Revisar esta documentación**
2. **Consultar archivos de código mencionados**
3. **Probar en modo debug** (`window.WhatsAppDebug`)
4. **Verificar consola del navegador** para errores

---

**Última actualización**: Enero 2024  
**Autor**: Equipo INGLAT  
**Versión**: 1.1