# Logo INGLAT Animado - Documentación

## 📁 Archivos Incluidos

```
logo/
├── inglat-logo-animated.svg          # SVG animado para redes sociales
├── inglat-logo-component.html        # Componente HTML standalone  
└── README.md                         # Esta documentación
```

---

## 🎨 Especificaciones del Logo

### **Colores**
- **Texto INGLAT**: `#006466` (Caribbean Current)
- **Electrones Dorados**: `#FFB627` (Accent Gold) 
- **Electrones Azules**: `#212f45` (Prussian Blue)

### **Animaciones**
- **6 electrones total**: 3 dorados (rápidos, 3s) + 3 azules (lentos, 6s)
- **6 patrones de movimiento** diferentes alrededor del texto
- **Efecto destello**: Box-shadow pulsante cada 2 segundos
- **Movimientos no circulares**: Ondas, zigzag, elipses, curvas S, rectangulares, espirales

---

## 📱 Uso en Redes Sociales

### **SVG Animado (`inglat-logo-animated.svg`)**

#### **Instagram**
- ✅ **Stories**: Tamaño recomendado 400x240px
- ✅ **Posts cuadrados**: Redimensionar a 300x180px
- ✅ **Reels**: Usar como overlay, tamaño 200x120px

#### **Facebook** 
- ✅ **Posts**: Tamaño original 200x60px
- ✅ **Cover**: Redimensionar a 400x240px 
- ✅ **Ads**: Escala automáticamente

#### **LinkedIn**
- ✅ **Posts**: Tamaño original perfecto
- ✅ **Company banner**: Redimensionar a 300x180px
- ✅ **Artículos**: Como imagen destacada

#### **Twitter/X**
- ✅ **Tweets**: Tamaño original
- ✅ **Header**: Redimensionar a 400x240px

---

## 🖥️ Uso del Componente HTML

### **Componente Standalone (`inglat-logo-component.html`)**

#### **Características**
- **Estilos embebidos**: Sin dependencias externas
- **Responsive**: Adaptable a cualquier dispositivo
- **Hover effect**: Pausa animación al pasar el mouse
- **Accesibilidad**: Respeta `prefers-reduced-motion`

#### **Casos de uso**
1. **Capturas de pantalla**: Abrir en navegador y capturar
2. **Presentaciones**: Usar como iframe embedded
3. **Email marketing**: Exportar como imagen
4. **Material publicitario**: Base para diseño gráfico

#### **Cómo usar**
```html
<!-- Opción 1: Iframe -->
<iframe src="static/images/logo/inglat-logo-component.html" 
        width="300" height="150" frameborder="0"></iframe>

<!-- Opción 2: Copiar CSS al proyecto -->
<div class="logo-inglat">
    <span class="logo-text">INGLAT</span>
    <!-- ... electrones ... -->
</div>
```

---

## 🛠️ Integración Técnica

### **En la Aplicación Django**

El logo principal está integrado en:
- `templates/base/header.html` (estructura HTML)
- `static/css/header.css` (animaciones CSS)
- `static/css/base.css` (estilos base)

### **Archivos del sistema**
```python
# En templates
{% load static %}
<img src="{% static 'images/logo/inglat-logo-animated.svg' %}" 
     alt="INGLAT Logo" width="200" height="60">
```

---

## 📐 Dimensiones Recomendadas

### **Para diferentes plataformas:**

| Plataforma | Tamaño Recomendado | Uso |
|-----------|-------------------|-----|
| Instagram Stories | 400x240px | Overlay o sticker |
| Instagram Posts | 300x180px | Logo en imagen |
| Facebook Cover | 400x240px | Banner de página |
| LinkedIn Posts | 200x60px | Original |
| Twitter Header | 400x240px | Banner de perfil |
| Email Signature | 150x45px | Firma corporativa |
| Presentaciones | 300x180px | Slides corporativos |

---

## 🎯 Mejores Prácticas

### **Exportación de Imágenes**
1. **Para GIF**: Usar ScreenToGif o LICEcap (6-9s de duración)
2. **Para PNG estático**: Capturar en momento específico de la animación
3. **Para vectorial**: Usar el SVG directamente

### **Rendimiento**
- **Animaciones CSS**: Más eficientes que JavaScript
- **Will-change**: Optimización GPU activada
- **Reduce-motion**: Cumple estándares de accesibilidad

### **Responsive**
- **Desktop**: 6 electrones completos
- **Tablet**: 6 electrones con movimientos reducidos  
- **Mobile**: Movimientos simplificados

---

## 🔧 Personalización

### **Cambiar colores**
```css
.electron--gold { background-color: #TU_COLOR; }
.electron--blue { background-color: #TU_COLOR; }
.logo-text { color: #TU_COLOR; }
```

### **Ajustar velocidades**
```css
.electron--gold { animation-duration: 3s; }  /* Más rápido */
.electron--blue { animation-duration: 6s; }  /* Más lento */
```

### **Modificar intensidad del destello**
```css
@keyframes glow-gold {
    50% { box-shadow: 0 0 15px rgba(255, 182, 39, 1); } /* Más intenso */
}
```

---

## 📞 Soporte

Para modificaciones adicionales del logo o integración en nuevas plataformas, consultar con el equipo de desarrollo.

**Versión**: 2.0  
**Última actualización**: Enero 2025  
**Compatible con**: Todos los navegadores modernos, redes sociales principales