// JavaScript para la página de inicio - Home Page
document.addEventListener('DOMContentLoaded', function() {
    
    // Video Loading Management
    function handleVideoLoading() {
        const videoLoading = document.getElementById('video-loading');
        const heroVideo = document.getElementById('hero-video');
        
        if (!videoLoading || !heroVideo) return;
        
        // Función para ocultar el loading
        const hideLoading = () => {
            videoLoading.classList.add('hidden');
        };
        
        // Para videos HTML5
        if (heroVideo.tagName === 'VIDEO') {
            heroVideo.addEventListener('loadeddata', hideLoading);
            heroVideo.addEventListener('canplay', hideLoading);
        }
        
        // Para iframes (YouTube, Vimeo, etc.)
        if (heroVideo.tagName === 'IFRAME') {
            heroVideo.addEventListener('load', () => {
                // Esperar un poco más para que el contenido del iframe se cargue
                setTimeout(hideLoading, 2000);
            });
            
            // Fallback: ocultar después de 5 segundos máximo
            setTimeout(hideLoading, 5000);
        }
    }
    
    // Inicializar loading management
    handleVideoLoading();
    
    // Hero Video Autoplay Enhancement
    function enhanceVideoAutoplay() {
        const heroVideo = document.getElementById('hero-video');
        if (!heroVideo) return;
        
        // Para videos HTML5 nativos
        if (heroVideo.tagName === 'VIDEO') {
            // Intentar reproducir cuando el usuario interactúe
            const tryPlay = () => {
                heroVideo.play().catch(error => {
                    console.log('Autoplay prevented:', error);
                });
            };
            
            // Intentar autoplay después de interacción del usuario
            ['click', 'touchstart'].forEach(event => {
                document.addEventListener(event, tryPlay, { once: true });
            });
        }
        
        // Para iframes de YouTube - usar YouTube API si está disponible
        if (heroVideo.tagName === 'IFRAME' && heroVideo.src.includes('youtube.com')) {
            heroVideo.addEventListener('load', function() {
                // El autoplay ya está configurado en la URL del iframe
                console.log('YouTube video loaded with autoplay settings');
            });
        }
    }
    
    // Inicializar mejoras de video
    enhanceVideoAutoplay();
    
    // Hyperspeed Starfield Effect Controller
    class HyperspeedStarfield {
        constructor(canvasId, config = {}) {
            this.canvas = document.getElementById(canvasId);
            if (!this.canvas) return;
            
            this.ctx = this.canvas.getContext('2d');
            this.stars = [];
            this.animationId = null;
            this.isRunning = false;
            
            // Configuration with mobile optimization
            this.config = {
                starCount: window.innerWidth < 768 ? 100 : 200,
                speed: config.speed || 2,
                maxSpeed: config.maxSpeed || 15,
                acceleration: config.acceleration || 0.02,
                starColors: ['#ffffff', '#b3d9ff', '#ffffcc', '#ffcccc'],
                minSize: 0.5,
                maxSize: 3,
                trailLength: 0.1,
                ...config
            };
            
            this.centerX = 0;
            this.centerY = 0;
            this.mouseX = 0;
            this.mouseY = 0;
            
            this.init();
        }
        
        init() {
            this.resize();
            this.createStars();
            this.setupEventListeners();
            this.start();
        }
        
        resize() {
            const rect = this.canvas.parentElement.getBoundingClientRect();
            this.canvas.width = rect.width;
            this.canvas.height = rect.height;
            this.centerX = this.canvas.width / 2;
            this.centerY = this.canvas.height / 2;
            
            // Mobile optimization: adjust star count based on screen size
            if (window.innerWidth < 768) {
                this.config.starCount = 100;
                this.config.speed = 1.5;
            } else if (window.innerWidth < 1024) {
                this.config.starCount = 150;
                this.config.speed = 2;
            } else {
                this.config.starCount = 200;
                this.config.speed = 2.5;
            }
        }
        
        createStars() {
            this.stars = [];
            for (let i = 0; i < this.config.starCount; i++) {
                this.stars.push(this.createStar());
            }
        }
        
        createStar() {
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * Math.min(this.centerX, this.centerY);
            
            return {
                x: Math.cos(angle) * distance,
                y: Math.sin(angle) * distance,
                z: Math.random() * 1000 + 1,
                prevX: 0,
                prevY: 0,
                color: this.config.starColors[Math.floor(Math.random() * this.config.starColors.length)],
                size: Math.random() * (this.config.maxSize - this.config.minSize) + this.config.minSize,
                speed: Math.random() * this.config.speed + 0.5
            };
        }
        
        setupEventListeners() {
            // Window resize handler
            window.addEventListener('resize', () => {
                this.resize();
                this.createStars();
            });
            
            // Mouse interaction for desktop
            if (!window.matchMedia('(max-width: 768px)').matches) {
                this.canvas.addEventListener('mousemove', (e) => {
                    const rect = this.canvas.getBoundingClientRect();
                    this.mouseX = (e.clientX - rect.left - this.centerX) / this.centerX;
                    this.mouseY = (e.clientY - rect.top - this.centerY) / this.centerY;
                });
                
                this.canvas.addEventListener('mouseleave', () => {
                    this.mouseX = 0;
                    this.mouseY = 0;
                });
            }
            
            // Visibility API - pause animation when page is hidden
            document.addEventListener('visibilitychange', () => {
                if (document.hidden) {
                    this.pause();
                } else {
                    this.start();
                }
            });
            
            // Respect reduced motion preference
            const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
            this.handleReducedMotion(mediaQuery);
            mediaQuery.addListener(this.handleReducedMotion.bind(this));
        }
        
        handleReducedMotion(mediaQuery) {
            if (mediaQuery.matches) {
                this.pause();
                this.canvas.style.display = 'none';
            } else {
                this.canvas.style.display = 'block';
                this.start();
            }
        }
        
        updateStar(star) {
            // Store previous position for trail effect
            star.prevX = star.x / star.z * 200 + this.centerX;
            star.prevY = star.y / star.z * 200 + this.centerY;
            
            // Move star closer (hyperspeed effect)
            star.z -= star.speed * this.config.speed;
            
            // Add mouse interaction influence (desktop only)
            if (!window.matchMedia('(max-width: 768px)').matches) {
                star.z -= (this.mouseX * this.mouseX + this.mouseY * this.mouseY) * 5;
            }
            
            // Reset star when it passes the camera
            if (star.z <= 0) {
                Object.assign(star, this.createStar());
                star.z = 1000;
            }
        }
        
        drawStar(star) {
            // Calculate screen position
            const x = star.x / star.z * 200 + this.centerX;
            const y = star.y / star.z * 200 + this.centerY;
            
            // Calculate star size based on distance
            const size = (1 - star.z / 1000) * star.size * 2;
            const opacity = Math.min(1, (1000 - star.z) / 300);
            
            // Skip stars that are too far or off-screen
            if (size < 0.1 || x < 0 || x > this.canvas.width || y < 0 || y > this.canvas.height) {
                return;
            }
            
            this.ctx.save();
            
            // Draw trail line for speed effect
            if (star.prevX && star.prevY && star.z < 800) {
                this.ctx.strokeStyle = `${star.color}${Math.floor(opacity * 0.3 * 255).toString(16).padStart(2, '0')}`;
                this.ctx.lineWidth = size * 0.5;
                this.ctx.lineCap = 'round';
                this.ctx.beginPath();
                this.ctx.moveTo(star.prevX, star.prevY);
                this.ctx.lineTo(x, y);
                this.ctx.stroke();
            }
            
            // Draw star
            this.ctx.fillStyle = `${star.color}${Math.floor(opacity * 255).toString(16).padStart(2, '0')}`;
            this.ctx.shadowBlur = size * 2;
            this.ctx.shadowColor = star.color;
            this.ctx.beginPath();
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
            this.ctx.fill();
            
            this.ctx.restore();
        }
        
        animate() {
            if (!this.isRunning) return;
            
            // Clear canvas with trail effect
            this.ctx.fillStyle = `rgba(26, 26, 46, ${this.config.trailLength})`;
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            
            // Update and draw all stars
            this.stars.forEach(star => {
                this.updateStar(star);
                this.drawStar(star);
            });
            
            this.animationId = requestAnimationFrame(() => this.animate());
        }
        
        start() {
            if (this.isRunning) return;
            this.isRunning = true;
            this.animate();
        }
        
        pause() {
            this.isRunning = false;
            if (this.animationId) {
                cancelAnimationFrame(this.animationId);
                this.animationId = null;
            }
        }
        
        destroy() {
            this.pause();
            window.removeEventListener('resize', this.resize);
            if (this.canvas) {
                this.canvas.removeEventListener('mousemove', () => {});
                this.canvas.removeEventListener('mouseleave', () => {});
            }
        }
    }
    
    // Initialize Hyperspeed Starfield
    const starfield = new HyperspeedStarfield('starfield-canvas', {
        speed: 2,
        starCount: window.innerWidth < 768 ? 100 : 200
    });
    
    // Enhanced CTA interaction
    const ctaButtons = document.querySelectorAll('.btn--accent');
    ctaButtons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            if (starfield && !window.matchMedia('(max-width: 768px)').matches) {
                starfield.config.speed *= 1.5;
            }
        });
        
        button.addEventListener('mouseleave', () => {
            if (starfield && !window.matchMedia('(max-width: 768px)').matches) {
                starfield.config.speed /= 1.5;
            }
        });
    });
    
    // Animación de números en las estadísticas
    const statNumbers = document.querySelectorAll('.stat-item__number');
    
    const animateNumbers = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = target.textContent;
                const numValue = parseInt(finalValue.replace(/[^\d]/g, ''));
                const suffix = finalValue.replace(/[\d]/g, '');
                
                let current = 0;
                const increment = Math.ceil(numValue / 50);
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= numValue) {
                        current = numValue;
                        clearInterval(timer);
                    }
                    target.textContent = current + suffix;
                }, 30);
                
                observer.unobserve(target);
            }
        });
    };
    
    const observer = new IntersectionObserver(animateNumbers, {
        threshold: 0.5
    });
    
    statNumbers.forEach(num => observer.observe(num));
    
    // === TARJETAS DE SERVICIOS EXPANDIBLES - VERSIÓN SIMPLIFICADA ===
    
    
    // Función simple para inicializar tarjetas
    function initServiceCards() {
        const cards = document.querySelectorAll('.service-card__details');
        const buttons = document.querySelectorAll('.service-card__toggle');
        
        
        // Asegurar que todas las tarjetas estén colapsadas
        cards.forEach((card, i) => {
            card.classList.remove('show');
            card.style.maxHeight = '0px';
        });
        
        // Inicializar botones  
        buttons.forEach((btn, i) => {
            btn.setAttribute('aria-expanded', 'false');
            const text = btn.querySelector('.toggle-text');
            const icon = btn.querySelector('.toggle-icon');
            if (text) text.textContent = 'Ver más';
            if (icon) icon.style.transform = 'rotate(0deg)';
        });
    }
    
    // Función simple de toggle
    function toggleCard(button) {
        const serviceType = button.getAttribute('data-toggle');
        const card = document.getElementById(`details-${serviceType}`);
        
        
        if (!card) {
            console.error(`❌ No se encontró: details-${serviceType}`);
            return;
        }
        
        const isExpanded = button.getAttribute('aria-expanded') === 'true';
        const text = button.querySelector('.toggle-text');
        const icon = button.querySelector('.toggle-icon');
        
        if (isExpanded) {
            // COLAPSAR
            button.setAttribute('aria-expanded', 'false');
            card.setAttribute('aria-hidden', 'true');
            card.classList.remove('show');
            card.style.maxHeight = '0px';
            if (text) text.textContent = 'Ver más';
            if (icon) icon.style.transform = 'rotate(0deg)';
        } else {
            // EXPANDIR  
            button.setAttribute('aria-expanded', 'true');
            card.setAttribute('aria-hidden', 'false');
            card.classList.add('show');
            
            // Calcular altura real del contenido
            const content = card.querySelector('.service-detail__content');
            if (content) {
                const height = content.scrollHeight + 40; // +40px padding
                card.style.maxHeight = `${height}px`;
            }
            
            if (text) text.textContent = 'Ver menos';
            if (icon) icon.style.transform = 'rotate(180deg)';
        }
    }
    
    // Configurar event listeners
    function setupCardListeners() {
        const buttons = document.querySelectorAll('.service-card__toggle');
        
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                toggleCard(this);
            });
            
            // Soporte teclado
            button.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleCard(this);
                }
            });
        });
        
    }
    
    // EJECUTAR INMEDIATAMENTE (tenemos defer en el script)
    initServiceCards();
    setupCardListeners();
    
    
    // Smooth scroll para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Funcionalidad para las tarjetas expandibles de proyectos
    const projectCards = document.querySelectorAll('.project-card');
    
    projectCards.forEach(card => {
        const toggleButton = card.querySelector('.project-card__toggle');
        const detailsPanel = card.querySelector('.project-card__details');
        
        if (toggleButton && detailsPanel) {
            toggleButton.addEventListener('click', function() {
                const isExpanded = this.getAttribute('aria-expanded') === 'true';
                const newState = !isExpanded;
                
                // Actualizar estados de accesibilidad
                this.setAttribute('aria-expanded', newState);
                detailsPanel.setAttribute('aria-hidden', !newState);
                
                // Agregar/remover clase para animación CSS
                if (newState) {
                    detailsPanel.style.maxHeight = detailsPanel.scrollHeight + 'px';
                    card.classList.add('project-card--expanded');
                } else {
                    detailsPanel.style.maxHeight = '0';
                    card.classList.remove('project-card--expanded');
                }
                
                // Scroll suave hacia la tarjeta si se está expandiendo
                if (newState && window.innerWidth > 768) {
                    setTimeout(() => {
                        card.scrollIntoView({
                            behavior: 'smooth',
                            block: 'nearest'
                        });
                    }, 150);
                }
            });
            
            // Soporte para navegación por teclado
            toggleButton.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.click();
                }
            });
        }
    });
    
    // Animación de aparición en scroll para las tarjetas de proyectos
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                cardObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Inicializar animación de aparición
    projectCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        cardObserver.observe(card);
    });
    
    // Cerrar tarjetas expandidas al hacer clic fuera (solo desktop)
    if (window.innerWidth > 768) {
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.project-card')) {
                projectCards.forEach(card => {
                    const toggleButton = card.querySelector('.project-card__toggle');
                    const detailsPanel = card.querySelector('.project-card__details');
                    
                    if (toggleButton && detailsPanel && toggleButton.getAttribute('aria-expanded') === 'true') {
                        toggleButton.setAttribute('aria-expanded', 'false');
                        detailsPanel.setAttribute('aria-hidden', 'true');
                        detailsPanel.style.maxHeight = '0';
                        card.classList.remove('project-card--expanded');
                    }
                });
            }
        });
    }
    
    // ===== MODAL DE COMPONENTES SOLARES =====
    
    // Datos técnicos detallados de cada componente
    const componentData = {
        'fuente-energia': {
            title: 'Fuente de Energía Solar',
            image: '/media/imagenes_animacion/fuente_energia.png',
            description: 'El Sol es la fuente de energía más abundante y sostenible disponible en la Tierra. Cada hora, la superficie terrestre recibe más energía solar de la que toda la humanidad consume en un año entero. Esta radiación electromagnética se convierte en electricidad mediante tecnología fotovoltaica, proporcionando una solución energética limpia, renovable e inagotable.',
            functionality: 'Como fuente primaria del sistema fotovoltaico, el Sol proporciona la energía radiante que los paneles solares convierten directamente en electricidad mediante el efecto fotovoltaico. La radiación solar varía según la hora del día, estación del año, ubicación geográfica y condiciones meteorológicas, por lo que es fundamental dimensionar correctamente el sistema para optimizar la captación energética.',
            features: [
                'Recurso energético completamente gratuito y renovable',
                'Disponibilidad diaria promedio de 4-6 horas de sol pico',
                'Potencial energético de 1.000 W/m² en condiciones ideales',
                'Sin emisiones de gases de efecto invernadero',
                'Independencia de fluctuaciones en precios de combustibles fósiles',
                'Vida útil ilimitada del recurso solar'
            ]
        },
        'paneles-solares': {
            title: 'Paneles Solares Fotovoltaicos',
            image: '/media/imagenes_animacion/panel_solar.png',
            description: 'Los paneles solares fotovoltaicos son dispositivos semiconductores que convierten directamente la radiación solar en electricidad mediante el efecto fotovoltaico. Fabricados principalmente con células de silicio cristalino o tecnologías de película delgada, estos módulos representan el corazón de cualquier instalación solar residencial.',
            functionality: 'Cada panel solar contiene múltiples células fotovoltaicas conectadas en serie y paralelo para generar el voltaje y corriente deseados. Cuando la luz solar incide sobre las células, los fotones liberan electrones en el material semiconductor, creando un flujo de corriente continua. Los paneles se conectan en serie para formar strings, aumentando el voltaje total del sistema.',
            features: [
                'Eficiencia de conversión entre 18-22% en paneles monocristalinos',
                'Vida útil garantizada de 25-30 años con degradación < 0.5% anual',
                'Potencia típica de 300-500W por panel residencial',
                'Resistencia a condiciones climáticas extremas (granizo, viento, lluvia)',
                'Tecnología anti-reflectante para máxima captación solar',
                'Certificaciones internacionales IEC 61215 e IEC 61730'
            ]
        },
        'estructura': {
            title: 'Estructura de Soporte de Aluminio',
            image: '/media/imagenes_animacion/estructura_solar.png',
            description: 'La estructura de soporte es el sistema de anclaje que fija los paneles solares al tejado o superficie de instalación. Fabricada en aleaciones de aluminio marino con tratamiento anodizado, garantiza la estabilidad, orientación óptima y durabilidad de toda la instalación solar durante décadas.',
            functionality: 'Proporciona el soporte mecánico necesario para mantener los paneles en la orientación e inclinación óptimas (generalmente 30-35° para captar la mayor cantidad de radiación solar posible). La estructura debe resistir cargas de viento, nieve y peso propio, distribuyendo uniformemente las fuerzas sobre la cubierta sin comprometer la estanqueidad del tejado.',
            features: [
                'Aleación de aluminio marino AA6005-T5 resistente a corrosión',
                'Diseño calculado para resistir vientos de hasta 150 km/h',
                'Sistema de fijación ajustable para diferentes tipos de tejado',
                'Garantía estructural de 20 años contra defectos de fabricación',
                'Instalación sin perforación del tejado mediante ganchas especiales',
                'Cumplimiento del Código Técnico de Edificación'
            ]
        },
        'inversor': {
            title: 'Inversor Solar Inteligente',
            image: '/media/imagenes_animacion/inversor_solar.png',
            description: 'El inversor es el cerebro de la instalación solar, responsable de convertir la corriente continua (DC) generada por los paneles solares en corriente alterna (AC) compatible con la red eléctrica doméstica. Los inversores modernos incorporan sistemas de monitorización avanzada, optimizadores de potencia y funciones de seguridad integradas.',
            functionality: 'Mediante circuitos electrónicos de potencia y algoritmos de seguimiento del punto de máxima potencia (MPPT), el inversor optimiza continuamente la extracción de energía de los paneles solares. También gestiona la sincronización con la red eléctrica, controla la calidad de la energía suministrada y proporciona protecciones contra sobretensiones, cortocircuitos y desconexión de red.',
            features: [
                'Eficiencia de conversión superior al 97% en inversores modernos',
                'Doble seguidor MPPT para optimización independiente de strings',
                'Monitorización en tiempo real vía WiFi/Ethernet',
                'Protecciones integradas: anti-islanding, sobretensión, cortocircuito',
                'Garantía del fabricante de 10-25 años según modelo',
                'Cumplimiento normativas internacionales'
            ]
        },
        'contador': {
            title: 'Contador Bidireccional Inteligente',
            image: '/media/imagenes_animacion/medidor_bidireccional.png',
            description: 'El contador bidireccional es un dispositivo de medición avanzado que registra tanto el consumo de electricidad de la red como la energía excedentaria inyectada por la instalación solar. Este equipo digital permite la implementación del autoconsumo con compensación de excedentes, optimizando el aprovechamiento económico de la producción solar.',
            functionality: 'Mide en tiempo real los flujos energéticos en ambas direcciones: consumo desde la red y excedentes vertidos a la red. Los datos se registran en diferentes períodos tarifarios, permitiendo el cálculo preciso de la compensación económica. La comunicación remota con la compañía eléctrica facilita la lectura automática y facturación del balance neto energético.',
            features: [
                'Medición bidireccional con precisión clase 1 según normativa',
                'Registro horario de consumo y generación para facturación',
                'Comunicación remota PLC/GPRS con distribuidora eléctrica',
                'Display LCD con información en tiempo real del balance energético',
                'Función anti-fraude y registro de eventos de red',
                'Homologación según normativa internacional'
            ]
        },
        'cargador': {
            title: 'Cargador para Vehículo Eléctrico',
            image: '/media/imagenes_animacion/cargador_vehiculo.png',
            description: 'El cargador de vehículo eléctrico es una estación de recarga doméstica que permite cargar automóviles eléctricos utilizando la energía solar generada por la instalación fotovoltaica. Estos dispositivos inteligentes optimizan la carga según la disponibilidad de energía solar, maximizando el autoconsumo y reduciendo los costes de movilidad.',
            functionality: 'Gestiona la recarga del vehículo eléctrico priorizando el uso de energía solar disponible. Los modelos inteligentes ajustan automáticamente la potencia de carga según la producción fotovoltaica instantánea, evitando el consumo innecesario de la red eléctrica. Incluye protecciones eléctricas, control de acceso y monitorización de sesiones de carga.',
            features: [
                'Potencia de carga ajustable desde 3.7kW hasta 22kW trifásico',
                'Carga inteligente con priorización de energía solar',
                'Control remoto vía aplicación móvil WiFi/4G',
                'Protecciones integradas: diferencial tipo A, magnetotérmico',
                'Compatible con todos los vehículos eléctricos (conector tipo 2)',
                'Certificación CE y cumplimiento normativa internacional'
            ]
        },
        'bateria': {
            title: 'Batería de Almacenamiento Solar',
            image: '/media/imagenes_animacion/bateria_solar.png',
            description: 'Las baterías de almacenamiento permiten acumular la energía solar excedentaria durante las horas de mayor producción para utilizarla posteriormente cuando no hay generación fotovoltaica. Las modernas baterías de ion-litio ofrecen alta densidad energética, miles de ciclos de vida útil y gestión inteligente de la energía almacenada.',
            functionality: 'Durante el día, cuando la producción solar supera el consumo instantáneo, la batería se carga automáticamente con el excedente energético. Por la noche o en días nublados, la batería suministra electricidad almacenada, reduciendo significativamente la dependencia de la red eléctrica. El sistema de gestión de batería (BMS) optimiza los ciclos de carga/descarga para maximizar la vida útil.',
            features: [
                'Tecnología ion-litio LiFePO4 con más de 6.000 ciclos de vida',
                'Capacidad típica de 5-15 kWh para instalaciones residenciales',
                'Eficiencia de carga/descarga superior al 95%',
                'Sistema de gestión de batería (BMS) con protecciones integradas',
                'Profundidad de descarga del 90-95% sin afectar la vida útil',
                'Garantía de rendimiento de 10 años con retención > 80% capacidad'
            ]
        }
    };
    
    // Variables del modal
    const modal = document.getElementById('component-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalImage = document.getElementById('modal-image');
    const modalDescription = document.getElementById('modal-description');
    const modalFunctionality = document.getElementById('modal-functionality');
    const modalFeatures = document.getElementById('modal-features');
    const modalCloseBtn = modal.querySelector('.component-modal__close');
    const modalBackdrop = modal.querySelector('.component-modal__backdrop');
    
    // Función para abrir el modal
    function openComponentModal(componentKey) {
        const data = componentData[componentKey];
        if (!data) {
            console.error(`No se encontraron datos para el componente: ${componentKey}`);
            return;
        }
        
        // Llenar el contenido del modal
        modalTitle.textContent = data.title;
        modalImage.src = data.image;
        modalImage.alt = data.title;
        modalDescription.textContent = data.description;
        modalFunctionality.textContent = data.functionality;
        
        // Llenar la lista de características
        modalFeatures.innerHTML = '';
        data.features.forEach(feature => {
            const li = document.createElement('li');
            li.textContent = feature;
            modalFeatures.appendChild(li);
        });
        
        // Mostrar el modal
        modal.classList.add('show');
        modal.setAttribute('aria-hidden', 'false');
        
        // Focus management para accesibilidad
        modalCloseBtn.focus();
        
        // Prevenir scroll del body (robusto y consistente con base.js)
        if (window.INGLAT && INGLAT.utils && typeof INGLAT.utils.lockBodyScroll === 'function') {
            INGLAT.utils.lockBodyScroll();
        } else {
            document.body.style.overflow = 'hidden';
        }
    }
    
    // Función para cerrar el modal
    function closeComponentModal() {
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        
        // Restaurar scroll del body
        if (window.INGLAT && INGLAT.utils && typeof INGLAT.utils.unlockBodyScroll === 'function') {
            INGLAT.utils.unlockBodyScroll();
        } else {
            document.body.style.overflow = '';
        }
        
        // Devolver focus al elemento que abrió el modal (si es posible)
        const activeLabel = document.querySelector('.component-label:focus');
        if (activeLabel) {
            activeLabel.focus();
        }
    }
    
    // Event listeners para los botones de componentes
    const componentLabels = document.querySelectorAll('.component-label');
    componentLabels.forEach(label => {
        // Click para abrir modal
        label.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const componentKey = this.getAttribute('data-component');
            openComponentModal(componentKey);
        });
        
        // Soporte para navegación por teclado
        label.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                e.stopPropagation();
                
                const componentKey = this.getAttribute('data-component');
                openComponentModal(componentKey);
            }
        });
        
        // Hacer focuseable para accesibilidad
        if (!label.hasAttribute('tabindex')) {
            label.setAttribute('tabindex', '0');
        }
    });
    
    // Event listeners para cerrar el modal
    modalCloseBtn.addEventListener('click', closeComponentModal);
    modalBackdrop.addEventListener('click', closeComponentModal);
    
    // Cerrar con tecla Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeComponentModal();
        }
    });
    
    // Trap focus dentro del modal cuando está abierto
    modal.addEventListener('keydown', function(e) {
        if (!modal.classList.contains('show')) return;
        
        if (e.key === 'Tab') {
            const focusableElements = modal.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];
            
            if (e.shiftKey) {
                // Shift + Tab
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                }
            } else {
                // Tab
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        }
    });
    
    // Prevenir que el modal se cierre si se hace click en el contenido
    modal.addEventListener('click', function(e) {
        if (e.target === modal || e.target === modalBackdrop) {
            closeComponentModal();
        }
    });
    
    // Evitar que clicks dentro del contenido cierren el modal y contener scroll
    (function(){
        const modalContent = modal.querySelector('.component-modal__content');
        if (!modalContent) return;
        modalContent.addEventListener('click', function(e) { e.stopPropagation(); });
        modalContent.addEventListener('touchmove', function(e) { e.stopPropagation(); }, { passive: true });
        modalContent.addEventListener('wheel', function(e) { e.stopPropagation(); }, { passive: true });
        // Mejorar experiencia de scroll en iOS/Android dentro del modal
        modalContent.style.overscrollBehavior = 'contain';
        modalContent.style.webkitOverflowScrolling = 'touch';
    })();
    
    // Performance monitoring (development only)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        let frameCount = 0;
        let lastTime = performance.now();
        
        const monitorPerformance = () => {
            frameCount++;
            const currentTime = performance.now();
            
            if (currentTime - lastTime >= 1000) {
                const fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
                console.log(`Starfield FPS: ${fps}`);
                frameCount = 0;
                lastTime = currentTime;
            }
            
            requestAnimationFrame(monitorPerformance);
        };
        
        monitorPerformance();
    }
});