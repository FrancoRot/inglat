# UI_UX_doc.md - Guía de Diseño INGLAT

## 🎨 Variables CSS Principales

### Paleta de Colores
```css
:root {
  /* Colores INGLAT */
  --primary-color: #006466;        /* Verde INGLAT */
  --primary-dark: #065a60;
  --primary-light: #008B8D;
  
  --secondary-color: #1b3a4b;      /* Carbón azulado */
  --accent-color: #FF6B35;         /* Naranja vibrante */
  --accent-gold: #FFB627;          /* Dorado premium */
  
  /* Neutros */
  --gray-900: #1A1A1A;
  --gray-500: #737373;
  --gray-100: #F5F5F5;
  --white: #FFFFFF;
  
  /* Funcionales */
  --success: #22C55E;
  --warning: #F59E0B;
  --error: #EF4444;
  
  /* Gradientes */
  --gradient-primary: linear-gradient(135deg, #006466 0%, #144552 100%);
  --gradient-accent: linear-gradient(135deg, #FF6B35 0%, #FFB627 100%);
  --gradient-hero: linear-gradient(135deg, #006466 0%, #1b3a4b 50%, #312244 100%);
}
```

### Tipografía
```css
:root {
  --font-primary: 'Inter', sans-serif;
  --font-secondary: 'Merriweather', serif;
  
  /* Tamaños comunes */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-4xl: 2.25rem;    /* 36px */
}
```

### Espaciado y Layout
```css
:root {
  --space-2: 0.5rem;      /* 8px */
  --space-4: 1rem;        /* 16px */
  --space-6: 1.5rem;      /* 24px */
  --space-8: 2rem;        /* 32px */
  --space-16: 4rem;       /* 64px */
  
  --border-radius: 0.5rem;        /* 8px */
  --border-radius-lg: 0.75rem;    /* 12px */
  
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
```

---

## 🔧 Componentes Base

### Botones Principales
```css
.btn {
  padding: var(--space-3) var(--space-6);
  border-radius: var(--border-radius);
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn--primary {
  background: var(--gradient-primary);
  color: var(--white);
}

.btn--simulator {
  background: var(--gradient-accent);
  color: var(--white);
}

.btn--whatsapp {
  background: #25D366;
  color: var(--white);
}

.btn--secondary {
  background: transparent;
  border: 2px solid var(--primary-color);
  color: var(--primary-color);
}
```

### Cards Básicas
```css
.card {
  background: var(--white);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
```

### Formularios
```css
.form-input {
  padding: var(--space-4);
  border: 2px solid var(--gray-300);
  border-radius: var(--border-radius);
  transition: all 0.3s ease;
}

.form-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 100, 102, 0.1);
}
```

---

## 🎯 Jerarquía de Botones

### Uso Recomendado
- **`.btn--primary`** (Verde INGLAT): CTAs principales, navegación
- **`.btn--simulator`** (Naranja): Simulador solar y funciones destacadas  
- **`.btn--whatsapp`** (Verde WhatsApp): Exclusivo para WhatsApp
- **`.btn--secondary`** (Borde): Acciones secundarias

### Modificadores
```css
.btn--small { padding: var(--space-2) var(--space-4); }
.btn--large { padding: var(--space-4) var(--space-8); }
```

---

## 📱 Responsive Design

### Breakpoints Principales
```css
/* Mobile */
@media (max-width: 768px) {
  .hero__title { font-size: var(--text-3xl); }
}

/* Desktop */
@media (min-width: 1024px) {
  .container { max-width: 1280px; }
}
```

---

## ✨ Layout Principal

### Header
```css
.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
}
```

### Hero Section
```css
.hero {
  background: var(--gradient-hero);
  color: var(--white);
  min-height: 100vh;
  text-align: center;
}

.hero__title {
  font-size: var(--text-5xl);
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9);
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  padding: var(--space-6);
  border-radius: var(--border-radius-lg);
}
```

### Footer
```css
.footer {
  background: var(--gradient-secondary);
  color: var(--gray-200);
  padding: var(--space-16) 0;
}
```

---

## 🎨 Principios de Diseño INGLAT

### Filosofía
- **Profesional**: Colores principales para transmitir confianza
- **Moderno**: Gradientes y efectos glassmorphism  
- **Accesible**: Contrastes WCAG 2.1 AA
- **Responsive**: Mobile-first approach

### Colores por Contexto
- **CTAs principales**: `--gradient-primary`
- **Simulador/destacados**: `--gradient-accent`  
- **WhatsApp**: `#25D366`
- **Información técnica**: `--secondary-color`

---

## 🔗 Referencias de Implementación

**Ubicación de archivos CSS**:
- `static/css/base.css` - Variables y estilos globales
- `static/css/header.css` - Estilos del header
- `static/css/footer.css` - Estilos del footer  
- `static/css/home.css` - Estilos específicos del home
- `static/css/simulador.css` - Estilos del simulador

**Uso en templates**:
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/home.css' %}">
```