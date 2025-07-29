// JavaScript para la página de inicio - Home Page
document.addEventListener('DOMContentLoaded', function() {
    
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