/**
 * INGLAT - JavaScript Base
 * Funcionalidades comunes para toda la aplicación
 */

'use strict';

// Namespace principal de INGLAT
const INGLAT = {
    // Configuración global
    config: {
        animationDuration: 300,
        breakpoints: {
            mobile: 768,
            tablet: 1024,
            desktop: 1280
        }
    },

    // Utilidades
    utils: {
        // Debounce function
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Throttle function
        throttle(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            }
        },

        // Detectar dispositivo móvil
        isMobile() {
            return window.innerWidth < this.breakpoints.mobile;
        },

        // Smooth scroll
        smoothScrollTo(target, offset = 0) {
            const element = typeof target === 'string' ? document.querySelector(target) : target;
            if (element) {
                const elementPosition = element.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - offset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        }
    },

    // Inicialización
    init() {
        this.mobileMenu.init();
        this.smoothScroll.init();
        this.contactButtons.init();
        this.animations.init();
        
        console.log('INGLAT JavaScript initialized');
    }
};

// Menú móvil
INGLAT.mobileMenu = {
    menuBtn: null,
    mobileMenu: null,
    overlay: null,
    isOpen: false,

    init() {
        this.menuBtn = document.querySelector('[data-menu-toggle]');
        this.mobileMenu = document.querySelector('#mobile-menu');
        this.overlay = document.querySelector('[data-menu-overlay]');

        if (this.menuBtn && this.mobileMenu && this.overlay) {
            this.bindEvents();
        }
    },

    bindEvents() {
        // Toggle menú
        this.menuBtn.addEventListener('click', () => this.toggle());
        
        // Cerrar con overlay
        this.overlay.addEventListener('click', () => this.close());
        
        // Cerrar con ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Cerrar al hacer click en links del menú
        const mobileLinks = this.mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                // Delay para permitir navegación antes de cerrar
                setTimeout(() => this.close(), 150);
            });
        });

        // Cerrar al cambiar tamaño de ventana (responsive)
        window.addEventListener('resize', INGLAT.utils.debounce(() => {
            if (window.innerWidth >= INGLAT.config.breakpoints.mobile && this.isOpen) {
                this.close();
            }
        }, 250));
    },

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    },

    open() {
        this.isOpen = true;
        this.mobileMenu.classList.add('active');
        this.overlay.classList.add('active');
        this.menuBtn.classList.add('active');
        this.menuBtn.setAttribute('aria-expanded', 'true');
        this.mobileMenu.setAttribute('aria-hidden', 'false');
        
        // Prevenir scroll del body
        document.body.style.overflow = 'hidden';
    },

    close() {
        this.isOpen = false;
        this.mobileMenu.classList.remove('active');
        this.overlay.classList.remove('active');
        this.menuBtn.classList.remove('active');
        this.menuBtn.setAttribute('aria-expanded', 'false');
        this.mobileMenu.setAttribute('aria-hidden', 'true');
        
        // Restaurar scroll del body
        document.body.style.overflow = '';
    }
};

// Smooth scroll para enlaces internos
INGLAT.smoothScroll = {
    init() {
        // Todos los enlaces que empiecen con #
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const href = anchor.getAttribute('href');
                
                // Ignorar enlaces vacíos o solo con #
                if (href === '#' || href === '') return;
                
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    // Offset para header sticky
                    const headerHeight = document.querySelector('.header')?.offsetHeight || 80;
                    INGLAT.utils.smoothScrollTo(target, headerHeight + 20);
                }
            });
        });
    }
};

// Botones de contacto flotantes o destacados
INGLAT.contactButtons = {
    init() {
        // WhatsApp floating button (si existe)
        const whatsappBtn = document.querySelector('.whatsapp-float');
        if (whatsappBtn) {
            this.initWhatsAppButton(whatsappBtn);
        }

        // Botones de teléfono con tracking
        const phoneButtons = document.querySelectorAll('a[href^="tel:"]');
        phoneButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Analytics tracking si está disponible
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'click', {
                        event_category: 'contact',
                        event_label: 'phone_call'
                    });
                }
            });
        });

        // Botones de WhatsApp con tracking
        const whatsappButtons = document.querySelectorAll('a[href*="wa.me"]');
        whatsappButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Analytics tracking si está disponible
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'click', {
                        event_category: 'contact',
                        event_label: 'whatsapp'
                    });
                }
            });
        });
    },

    initWhatsAppButton(button) {
        // Mostrar/ocultar based on scroll
        let isVisible = false;
        
        const toggleVisibility = INGLAT.utils.throttle(() => {
            const shouldShow = window.scrollY > 300;
            
            if (shouldShow && !isVisible) {
                button.classList.add('visible');
                isVisible = true;
            } else if (!shouldShow && isVisible) {
                button.classList.remove('visible');
                isVisible = false;
            }
        }, 100);

        window.addEventListener('scroll', toggleVisibility);
    }
};

// Animaciones básicas
INGLAT.animations = {
    init() {
        // Fade in elements cuando entran en viewport
        this.initFadeInAnimations();
        
        // Counter animations para números
        this.initCounterAnimations();
    },

    initFadeInAnimations() {
        const fadeElements = document.querySelectorAll('.fade-in');
        
        if (fadeElements.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        fadeElements.forEach(el => observer.observe(el));
    },

    initCounterAnimations() {
        const counters = document.querySelectorAll('.counter');
        
        if (counters.length === 0) return;

        const animateCounter = (counter) => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = parseInt(counter.getAttribute('data-duration')) || 2000;
            const increment = target / (duration / 16); // 60fps
            let current = 0;

            const updateCounter = () => {
                current += increment;
                if (current >= target) {
                    current = target;
                    counter.textContent = Math.floor(current);
                    return;
                }
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            };

            updateCounter();
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });

        counters.forEach(counter => observer.observe(counter));
    }
};

// Manejo de formularios (si es necesario)
INGLAT.forms = {
    init() {
        // Validación básica de formularios
        const forms = document.querySelectorAll('form[data-validate]');
        forms.forEach(form => this.initFormValidation(form));
    },

    initFormValidation(form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Aquí iría la lógica de validación
            // Por ahora solo previene el envío para evitar errores
            console.log('Form validation would happen here');
        });
    }
};

// Manejo de mensajes/alertas
INGLAT.messages = {
    init() {
        // Auto-hide messages después de cierto tiempo
        const messages = document.querySelectorAll('.alert');
        messages.forEach(message => {
            const closeBtn = message.querySelector('.alert__close');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => this.hideMessage(message));
            }

            // Auto-hide después de 5 segundos
            if (!message.classList.contains('alert--error')) {
                setTimeout(() => this.hideMessage(message), 5000);
            }
        });
    },

    hideMessage(message) {
        message.style.opacity = '0';
        message.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            message.remove();
        }, INGLAT.config.animationDuration);
    }
};

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    INGLAT.init();
    INGLAT.forms.init();
    INGLAT.messages.init();
});

// Exposición global para uso externo si es necesario
window.INGLAT = INGLAT;