# UI_UX_doc.md - Guía de Diseño INGLAT

## Paleta de Colores Principal

### Variables CSS Base
```css
:root {
  /* Paleta INGLAT - Colores base */
  --caribbean-current: #006466;       /* Verde azulado profundo */
  --midnight-green: #065a60;          /* Verde medianoche */
  --midnight-green-2: #0b525b;        /* Verde medianoche 2 */
  --midnight-green-3: #144552;        /* Verde medianoche 3 */
  --charcoal: #1b3a4b;                /* Carbón azulado */
  --prussian-blue: #212f45;           /* Azul prusiano */
  --space-cadet: #272640;             /* Azul espacial */
  --dark-purple: #312244;             /* Púrpura oscuro */
  --dark-purple-2: #3e1f47;           /* Púrpura oscuro 2 */
  --palatinate: #4d194d;              /* Púrpura palatino */
  
  /* Colores principales del sistema */
  --primary-color: var(--caribbean-current);
  --primary-dark: var(--midnight-green);
  --primary-light: #008B8D;
  --primary-lightest: #B3E0E1;
  
  --secondary-color: var(--charcoal);
  --secondary-dark: var(--prussian-blue);
  --secondary-light: #2A4A5C;
  --secondary-lightest: #C8D4DC;
  
  /* Colores de acento */
  --accent-color: #FF6B35;            /* Naranja vibrante */
  --accent-gold: #FFB627;             /* Dorado premium */
  
  /* Neutros */
  --gray-900: #1A1A1A;
  --gray-700: #404040;
  --gray-500: #737373;
  --gray-300: #D4D4D4;
  --gray-100: #F5F5F5;
  --white: #FFFFFF;
  
  /* Funcionales */
  --success: #22C55E;
  --warning: #F59E0B;
  --error: #EF4444;
  --info: var(--primary-light);
  
  /* Gradientes principales */
  --gradient-primary: linear-gradient(135deg, var(--caribbean-current) 0%, var(--midnight-green-3) 100%);
  --gradient-secondary: linear-gradient(135deg, var(--charcoal) 0%, var(--prussian-blue) 100%);
  --gradient-accent: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-gold) 100%);
  --gradient-hero: linear-gradient(135deg, var(--caribbean-current) 0%, var(--charcoal) 50%, var(--dark-purple) 100%);
  
  /* Sombras */
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-primary: 0 4px 14px 0 rgba(0, 100, 102, 0.15);
  --shadow-accent: 0 4px 14px 0 rgba(255, 107, 53, 0.25);
}
```

---

## Tipografía

```css
:root {
  /* Fuentes */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-secondary: 'Merriweather', Georgia, serif;
  
  /* Tamaños */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  --text-5xl: 3rem;       /* 48px */
  
  /* Pesos */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

---

## Espaciado y Layout

```css
:root {
  /* Espacios */
  --space-1: 0.25rem;     /* 4px */
  --space-2: 0.5rem;      /* 8px */
  --space-3: 0.75rem;     /* 12px */
  --space-4: 1rem;        /* 16px */
  --space-6: 1.5rem;      /* 24px */
  --space-8: 2rem;        /* 32px */
  --space-12: 3rem;       /* 48px */
  --space-16: 4rem;       /* 64px */
  --space-24: 6rem;       /* 96px */
  
  /* Contenedores */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1536px;
  
  /* Bordes */
  --border-radius: 0.5rem;        /* 8px */
  --border-radius-lg: 0.75rem;    /* 12px */
  --border-radius-xl: 1rem;       /* 16px */
}
```

---

## Componentes Base

### Botones
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  border-radius: var(--border-radius);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  font-family: inherit;
}

.btn--primary {
  background: var(--gradient-primary);
  color: var(--white);
  box-shadow: var(--shadow-primary);
}

.btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(0, 100, 102, 0.3);
}

.btn--secondary {
  background: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
}

.btn--secondary:hover {
  background: var(--primary-color);
  color: var(--white);
}

.btn--simulator {
  background: var(--gradient-accent);
  color: var(--white);
  box-shadow: var(--shadow-accent);
  font-weight: var(--font-semibold);
}

.btn--simulator:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(255, 107, 53, 0.4);
}

.btn--whatsapp {
  background: #25D366;
  color: var(--white);
  box-shadow: 0 4px 14px 0 rgba(37, 211, 102, 0.25);
}

.btn--whatsapp:hover {
  background: #20BD5A;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(37, 211, 102, 0.3);
}

.btn--call {
  background: var(--gradient-primary);
  color: var(--white);
  box-shadow: var(--shadow-primary);
}

.btn--call:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(0, 100, 102, 0.3);
}

.btn--accent {
  background: var(--gradient-accent);
  color: var(--white);
  box-shadow: var(--shadow-accent);
}

.btn--accent:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(255, 107, 53, 0.3);
}

/* Hero Actions - Botones uniformes */
.hero__actions .btn {
  min-width: 180px;
  padding: var(--space-4) var(--space-6);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
}
```

### Cards
```css
.card {
  background: var(--white);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid var(--gray-200);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-light);
}

.card__content {
  padding: var(--space-6);
}

.card__title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--gray-900);
  margin-bottom: var(--space-3);
}

.card:hover .card__title {
  color: var(--primary-color);
}
```

### Formularios
```css
.form-input {
  width: 100%;
  padding: var(--space-4);
  font-size: var(--text-base);
  border: 2px solid var(--gray-300);
  border-radius: var(--border-radius);
  background: var(--white);
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 100, 102, 0.1);
}

.form-label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--gray-700);
  margin-bottom: var(--space-2);
}
```

---

## Layout Principal

### Header
```css
.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px 0 rgba(0, 100, 102, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header__logo {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-decoration: none;
}

.header__nav-link {
  color: var(--gray-700);
  text-decoration: none;
  font-weight: var(--font-medium);
  transition: color 0.3s ease;
}

.header__nav-link:hover {
  color: var(--primary-color);
}
```

### Hero Section
```css
.hero {
  background: var(--gradient-hero);
  color: var(--white);
  padding: var(--space-24) 0;
  text-align: center;
  position: relative;
  overflow: hidden;
  min-height: 100vh;
}

.hero__title {
  font-size: var(--text-6xl);
  font-weight: var(--font-bold);
  color: var(--white);
  margin-bottom: var(--space-6);
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9), 0 0 20px rgba(0, 0, 0, 0.7);
  line-height: 1.2;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  padding: var(--space-6) var(--space-8);
  border-radius: var(--border-radius-xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.hero__subtitle {
  font-size: var(--text-2xl);
  color: var(--white);
  margin-bottom: var(--space-8);
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9), 0 0 20px rgba(0, 0, 0, 0.7);
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(10px);
  padding: var(--space-5) var(--space-6);
  border-radius: var(--border-radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.15);
  line-height: 1.5;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  font-weight: var(--font-medium);
}
```

### Footer
```css
.footer {
  background: var(--gradient-secondary);
  color: var(--gray-200);
  padding: var(--space-16) 0 var(--space-8);
}

.footer__section-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--white);
  margin-bottom: var(--space-4);
}

.footer__link {
  color: var(--gray-300);
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer__link:hover {
  color: var(--primary-light);
}
```

---

## Utilidades Principales

### Colores de Texto
```css
.text-primary { color: var(--primary-color); }
.text-secondary { color: var(--secondary-color); }
.text-accent { color: var(--accent-color); }
.text-gray-900 { color: var(--gray-900); }
.text-gray-700 { color: var(--gray-700); }
.text-white { color: var(--white); }
```

### Fondos
```css
.bg-primary { background-color: var(--primary-color); }
.bg-white { background-color: var(--white); }
.bg-gray-100 { background-color: var(--gray-100); }
.bg-gradient-primary { background: var(--gradient-primary); }
.bg-gradient-hero { background: var(--gradient-hero); }
```

### Espaciado
```css
.p-4 { padding: var(--space-4); }
.p-6 { padding: var(--space-6); }
.p-8 { padding: var(--space-8); }
.m-4 { margin: var(--space-4); }
.mb-6 { margin-bottom: var(--space-6); }
.mt-8 { margin-top: var(--space-8); }
```

---

## Responsive Design

```css
/* Mobile */
@media (max-width: 768px) {
  .hero__title {
    font-size: var(--text-3xl);
  }
  
  .header__nav {
    display: none; /* Implementar menú hamburguesa */
  }
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1023px) {
  .container {
    max-width: var(--container-md);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: var(--container-xl);
  }
}
```

---

## Notas de Implementación

### Orden de Implementación
1. **Variables CSS**: Implementar todas las variables base
2. **Componentes básicos**: Botones, cards, formularios
3. **Layout**: Header, footer, hero section
4. **Páginas específicas**: Según se vayan desarrollando

### Principios de Diseño INGLAT
- **Profesional**: Uso de la paleta principal para transmitir confianza
- **Moderno**: Gradientes y efectos glassmorphism
- **Accesible**: Contrastes WCAG 2.1 AA garantizados
- **Responsive**: Mobile-first approach

### Colores por Contexto
- **CTAs principales**: `--gradient-primary`
- **Información técnica**: `--secondary-color`
- **Ofertas/promociones**: `--accent-color`
- **Elementos premium**: `--accent-gold`

---

## Jerarquía de Botones INGLAT

### Guía de Uso de Botones

#### 🟢 `.btn--primary` - Verde INGLAT
**Uso:** CTAs principales, navegación principal, acciones primarias
**Color:** `var(--gradient-primary)` (#006466 → #144552)
**Ejemplo:** "Ver Proyectos", "Enviar Consulta", botones de formulario

#### 🟠 `.btn--simulator` - Naranja Destacado  
**Uso:** Simulador solar y funciones especiales destacadas
**Color:** `var(--gradient-accent)` (#FF6B35 → #FFB627)
**Ejemplo:** "Simulador Solar", CTAs de conversión especiales

#### ⚪ `.btn--secondary` - Borde Verde
**Uso:** Acciones secundarias, navegación alternativa
**Color:** Transparente con borde `var(--primary-color)`
**Ejemplo:** "Conocer Servicios", "Cancelar", acciones opcionales

#### 💚 `.btn--whatsapp` - Verde WhatsApp
**Uso:** Exclusivo para enlaces de WhatsApp
**Color:** `#25D366` (color oficial WhatsApp)
**Ejemplo:** Botones de contacto WhatsApp

#### 📞 `.btn--call` - Verde INGLAT  
**Uso:** Enlaces de llamada telefónica
**Color:** `var(--gradient-primary)` (igual que primary)
**Ejemplo:** Botones "Llamar"

#### ✨ `.btn--accent` - Gradiente Naranja
**Uso:** Promociones especiales, ofertas destacadas
**Color:** `var(--gradient-accent)` (#FF6B35 → #FFB627)
**Ejemplo:** "Oferta Especial", promociones limitadas

### Modificadores Adicionales
```css
.btn--small { padding: var(--space-2) var(--space-4); font-size: var(--text-sm); }
.btn--large { padding: var(--space-4) var(--space-8); font-size: var(--text-lg); }
```

---

## Accesibilidad y Contraste

### Texto sobre Imágenes en Movimiento
Para garantizar la legibilidad del texto sobre fondos dinámicos o imágenes:

```css
/* Fondo semitransparente con blur para texto sobre imágenes */
.text-over-image {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  padding: var(--space-4) var(--space-6);
  border-radius: var(--border-radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Text shadows para mejorar legibilidad */
.text-shadow-strong {
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9), 0 0 20px rgba(0, 0, 0, 0.7);
}
```

### Principios de Contraste INGLAT
- **Ratio mínimo**: 4.5:1 para texto normal
- **Ratio mínimo**: 3:1 para texto grande (>18px)
- **Texto blanco sobre fondo oscuro**: Siempre usar text-shadow para mayor legibilidad
- **Backdrop-filter**: Usar blur(8px-10px) para fondos semitransparentes
- **Fallbacks**: Proporcionar fondos sólidos alternativos para navegadores que no soporten backdrop-filter

### Responsive de Hero Section
```css
/* Mobile optimizations */
@media (max-width: 768px) {
  .hero__title {
    font-size: var(--text-4xl);
    padding: var(--space-4) var(--space-6);
    max-width: 95%;
  }
  
  .hero__subtitle {
    font-size: var(--text-lg);
    padding: var(--space-4) var(--space-5);
    max-width: 95%;
  }
}
```

---