/**
 * NOTICIAS.JS - Sistema de Blog INGLAT
 * Funcionalidades: Filtrado dinámico, animaciones, interacciones
 */

class NoticiasManager {
    constructor() {
        this.initElements();
        this.bindEvents();
        this.initAnimations();
    }

    initElements() {
        // Elementos de filtro
        this.searchInput = document.getElementById('search-input');
        this.categoriaSelect = document.getElementById('categoria-select');
        this.fechaSelect = document.getElementById('fecha-select');
        
        // Elementos de contenido
        this.noticiasGrid = document.getElementById('noticias-grid');
        this.loadingState = document.getElementById('loading-state');
        this.noticiasCount = document.getElementById('noticias-count');
        
        // Estado de filtros
        this.filtros = {
            categoria: 'todas',
            fecha: 'todas',
            busqueda: ''
        };
        
        // Configuración
        this.debounceDelay = 500;
        this.animationDelay = 100;
    }

    bindEvents() {
        // Filtro de búsqueda con debounce
        if (this.searchInput) {
            this.searchInput.addEventListener('input', this.debounce(() => {
                this.filtros.busqueda = this.searchInput.value.trim();
                this.aplicarFiltros();
            }, this.debounceDelay));
        }

        // Filtro de categoría
        if (this.categoriaSelect) {
            this.categoriaSelect.addEventListener('change', () => {
                this.filtros.categoria = this.categoriaSelect.value;
                this.aplicarFiltros();
            });
        }

        // Filtro de fecha
        if (this.fechaSelect) {
            this.fechaSelect.addEventListener('change', () => {
                this.filtros.fecha = this.fechaSelect.value;
                this.aplicarFiltros();
            });
        }

        // Animaciones de scroll
        window.addEventListener('scroll', this.throttle(() => {
            this.handleScrollAnimations();
        }, 100));

        // Hover effects en cards
        this.bindCardHoverEffects();
    }

    bindCardHoverEffects() {
        const cards = document.querySelectorAll('.noticia-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.animateCardHover(card, true);
            });
            
            card.addEventListener('mouseleave', () => {
                this.animateCardHover(card, false);
            });
        });
    }

    animateCardHover(card, isEntering) {
        const image = card.querySelector('.card-image');
        const leerMas = card.querySelector('.leer-mas');
        
        if (isEntering) {
            // Entrada del hover
            if (image) {
                image.style.transform = 'scale(1.05)';
            }
            if (leerMas) {
                const arrow = leerMas.querySelector('.fa-arrow-right');
                if (arrow) {
                    arrow.style.transform = 'translateX(4px)';
                }
            }
            
            // Animación sutil de elevación
            card.style.transform = 'translateY(-4px)';
            
        } else {
            // Salida del hover
            if (image) {
                image.style.transform = 'scale(1)';
            }
            if (leerMas) {
                const arrow = leerMas.querySelector('.fa-arrow-right');
                if (arrow) {
                    arrow.style.transform = 'translateX(0)';
                }
            }
            
            card.style.transform = 'translateY(0)';
        }
    }

    async aplicarFiltros() {
        if (!this.noticiasGrid) return;

        try {
            // Mostrar loading
            this.showLoading(true);

            // Preparar parámetros
            const params = new URLSearchParams();
            if (this.filtros.categoria !== 'todas') {
                params.append('categoria', this.filtros.categoria);
            }
            if (this.filtros.fecha !== 'todas') {
                params.append('fecha', this.filtros.fecha);
            }
            if (this.filtros.busqueda) {
                params.append('q', this.filtros.busqueda);
            }

            // Realizar petición AJAX
            const response = await fetch(`/noticias/filtrar/?${params.toString()}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Error en la petición');
            }

            const data = await response.json();
            
            // Actualizar contenido
            this.actualizarGrid(data.noticias);
            this.actualizarContador(data.total);

        } catch (error) {
            console.error('Error aplicando filtros:', error);
            this.mostrarError('Error al cargar las noticias. Por favor, recarga la página.');
        } finally {
            this.showLoading(false);
        }
    }

    actualizarGrid(noticias) {
        if (!this.noticiasGrid) return;

        // Animación de salida
        this.noticiasGrid.style.opacity = '0.5';
        this.noticiasGrid.style.transform = 'translateY(10px)';

        setTimeout(() => {
            if (noticias.length === 0) {
                this.mostrarMensajeVacio();
            } else {
                this.renderizarNoticias(noticias);
            }

            // Animación de entrada
            this.noticiasGrid.style.opacity = '1';
            this.noticiasGrid.style.transform = 'translateY(0)';
            
            // Re-bind hover effects
            this.bindCardHoverEffects();
            
            // Scroll suave al top del grid
            this.scrollToGrid();

        }, 200);
    }

    renderizarNoticias(noticias) {
        const html = noticias.map(noticia => this.generarCardHTML(noticia)).join('');
        this.noticiasGrid.innerHTML = html;

        // Animación staggered para las cards
        const cards = this.noticiasGrid.querySelectorAll('.noticia-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * this.animationDelay);
        });
    }

    generarCardHTML(noticia) {
        const mediaHTML = this.generarMediaHTML(noticia);
        const categoriaHTML = noticia.categoria ? 
            `<div class="card-categoria-badge" style="background-color: ${noticia.categoria.color};">
                <i class="fas fa-tag"></i>
                ${noticia.categoria.nombre}
            </div>` : '';

        return `
            <article class="noticia-card" data-categoria="${noticia.categoria?.slug || 'sin-categoria'}">
                <a href="${noticia.url}" class="card-link">
                    <div class="card-media">
                        ${mediaHTML}
                        ${categoriaHTML}
                    </div>
                    <div class="card-content">
                        <header class="card-header">
                            <h3 class="card-titulo">${noticia.titulo}</h3>
                            <div class="card-meta">
                                <time class="card-fecha">
                                    <i class="fas fa-calendar-alt"></i>
                                    ${noticia.fecha}
                                </time>
                                <span class="card-lectura">
                                    <i class="fas fa-clock"></i>
                                    ${noticia.tiempo_lectura}
                                </span>
                            </div>
                        </header>
                        <div class="card-body">
                            <p class="card-descripcion">${noticia.descripcion_corta}</p>
                        </div>
                        <footer class="card-footer">
                            <div class="card-autor">
                                <i class="fas fa-user"></i>
                                Equipo INGLAT
                            </div>
                            <div class="card-cta">
                                <span class="leer-mas">
                                    Leer más
                                    <i class="fas fa-arrow-right"></i>
                                </span>
                            </div>
                        </footer>
                    </div>
                </a>
            </article>
        `;
    }

    generarMediaHTML(noticia) {
        if (noticia.imagen_url) {
            return `<img src="${noticia.imagen_url}" alt="${noticia.titulo}" class="card-image" loading="lazy">`;
        }
        return `
            <div class="card-placeholder">
                <i class="fas fa-newspaper fa-2x"></i>
            </div>
        `;
    }

    mostrarMensajeVacio() {
        this.noticiasGrid.innerHTML = `
            <div class="no-noticias">
                <i class="fas fa-search fa-3x"></i>
                <h3>No se encontraron noticias</h3>
                <p>No hay noticias que coincidan con los filtros seleccionados.</p>
                <button class="btn btn--primary" onclick="noticiasManager.limpiarFiltros()">
                    <i class="fas fa-refresh"></i>
                    Limpiar Filtros
                </button>
            </div>
        `;
    }

    actualizarContador(total) {
        if (this.noticiasCount) {
            const texto = total === 1 ? 'noticia' : 'noticias';
            this.noticiasCount.textContent = `${total} ${texto}`;
        }
    }

    showLoading(show) {
        if (this.loadingState) {
            this.loadingState.style.display = show ? 'block' : 'none';
        }
    }

    mostrarError(mensaje) {
        if (this.noticiasGrid) {
            this.noticiasGrid.innerHTML = `
                <div class="error-state">
                    <i class="fas fa-exclamation-triangle fa-3x" style="color: var(--error);"></i>
                    <h3>Error</h3>
                    <p>${mensaje}</p>
                    <button class="btn btn--primary" onclick="location.reload()">
                        <i class="fas fa-refresh"></i>
                        Recargar
                    </button>
                </div>
            `;
        }
    }

    limpiarFiltros() {
        // Reset form elements
        if (this.searchInput) this.searchInput.value = '';
        if (this.categoriaSelect) this.categoriaSelect.value = 'todas';
        if (this.fechaSelect) this.fechaSelect.value = 'todas';

        // Reset internal state
        this.filtros = {
            categoria: 'todas',
            fecha: 'todas',
            busqueda: ''
        };

        // Apply filters
        this.aplicarFiltros();
    }

    scrollToGrid() {
        if (this.noticiasGrid) {
            const rect = this.noticiasGrid.getBoundingClientRect();
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const targetPosition = rect.top + scrollTop - 100; // 100px offset

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }

    initAnimations() {
        // Intersection Observer para animaciones de scroll
        if ('IntersectionObserver' in window) {
            this.setupScrollAnimations();
        }
    }

    setupScrollAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Observar elementos animables
        const animatableElements = document.querySelectorAll(
            '.noticia-card, .sidebar-section, .noticias-header'
        );
        
        animatableElements.forEach(el => {
            el.classList.add('animate-element');
            observer.observe(el);
        });
    }

    handleScrollAnimations() {
        // Paralax effect para hero (si existe)
        const hero = document.querySelector('.noticias-hero');
        if (hero) {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        }
    }

    // Utility functions
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
    }

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
        };
    }
}

// Función global para limpiar filtros (usada en templates)
function limpiarFiltros() {
    if (window.noticiasManager) {
        window.noticiasManager.limpiarFiltros();
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    window.noticiasManager = new NoticiasManager();
    
    // CSS para animaciones de scroll
    const style = document.createElement('style');
    style.textContent = `
        .animate-element {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s ease;
        }
        
        .animate-element.animate-in {
            opacity: 1;
            transform: translateY(0);
        }
        
        .error-state {
            text-align: center;
            padding: var(--space-16) var(--space-8);
            background: var(--white);
            border-radius: var(--border-radius-lg);
            box-shadow: var(--shadow);
            grid-column: 1 / -1;
        }
        
        .error-state i {
            margin-bottom: var(--space-4);
        }
        
        .error-state h3 {
            color: var(--gray-700);
            margin-bottom: var(--space-3);
        }
        
        .error-state p {
            color: var(--gray-600);
            margin-bottom: var(--space-6);
        }
        
        /* Animaciones adicionales */
        .noticia-card {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .card-image {
            transition: transform 0.3s ease;
        }
        
        .leer-mas .fa-arrow-right {
            transition: transform 0.3s ease;
        }
        
        .compartir-btn {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .compartir-btn:hover {
            transform: scale(1.1) rotate(5deg);
        }
        
        /* Loading spinner */
        .loading-state {
            text-align: center;
            padding: var(--space-8);
            grid-column: 1 / -1;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .fade-in-up {
            animation: fadeInUp 0.6s ease forwards;
        }
    `;
    document.head.appendChild(style);
});

// Utilidades adicionales para compartir en redes sociales
class SocialShare {
    static compartirTwitter(titulo, url) {
        const text = encodeURIComponent(titulo);
        const shareUrl = encodeURIComponent(url);
        window.open(`https://twitter.com/intent/tweet?text=${text}&url=${shareUrl}`, '_blank', 'width=600,height=400');
    }

    static compartirFacebook(url) {
        const shareUrl = encodeURIComponent(url);
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${shareUrl}`, '_blank', 'width=600,height=400');
    }

    static compartirLinkedIn(url) {
        const shareUrl = encodeURIComponent(url);
        window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${shareUrl}`, '_blank', 'width=600,height=400');
    }

    static compartirWhatsApp(titulo, url) {
        const text = encodeURIComponent(`${titulo} ${url}`);
        window.open(`https://wa.me/?text=${text}`, '_blank');
    }
}

// Exportar para uso global
window.SocialShare = SocialShare;

// ==========================================
// SISTEMA DE VIDEO UNIVERSAL
// ==========================================

class VideoManager {
    constructor() {
        this.videos = new Map();
        this.intersectionObserver = null;
        this.init();
    }
    
    init() {
        this.setupLazyLoading();
        this.setupVideoErrorHandling();
        this.setupVideoAnalytics();
        this.preloadVideoThumbnails();
    }
    
    // Configurar lazy loading para videos
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            this.intersectionObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.loadVideo(entry.target);
                        this.intersectionObserver.unobserve(entry.target);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.1
            });
            
            // Observar todos los contenedores de video
            document.querySelectorAll('.video-container[data-lazy="true"]').forEach(video => {
                this.intersectionObserver.observe(video);
            });
        }
    }
    
    // Cargar video cuando sea necesario
    loadVideo(container) {
        const videoUrl = container.dataset.videoUrl;
        const platform = container.dataset.platform;
        
        if (!videoUrl || !platform) return;
        
        // Mostrar loading
        container.classList.add('video-loading');
        
        // Crear iframe o elemento de video según la plataforma
        const mediaElement = this.createVideoElement(videoUrl, platform);
        
        if (mediaElement) {
            mediaElement.onload = () => {
                container.classList.remove('video-loading');
            };
            
            mediaElement.onerror = () => {
                this.handleVideoError(container, videoUrl, platform);
            };
            
            container.appendChild(mediaElement);
        }
    }
    
    // Crear elemento de video según la plataforma
    createVideoElement(url, platform) {
        const embedUrl = this.getEmbedUrl(url, platform);
        
        if (!embedUrl) return null;
        
        if (platform === 'direct' || platform === 'gdrive' || platform === 'dropbox') {
            // Video directo
            const video = document.createElement('video');
            video.src = embedUrl;
            video.controls = true;
            video.preload = 'metadata';
            video.className = 'video-direct';
            return video;
        } else {
            // Video embebido (YouTube, Vimeo)
            const iframe = document.createElement('iframe');
            iframe.src = embedUrl;
            iframe.className = 'video-iframe';
            iframe.frameBorder = '0';
            iframe.allowFullscreen = true;
            iframe.allow = 'autoplay; fullscreen; picture-in-picture';
            return iframe;
        }
    }
    
    // Obtener URL de embed según plataforma
    getEmbedUrl(url, platform) {
        const videoId = this.extractVideoId(url, platform);
        
        switch (platform) {
            case 'youtube':
                return videoId ? `https://www.youtube.com/embed/${videoId}` : null;
            case 'vimeo':
                return videoId ? `https://player.vimeo.com/video/${videoId}` : null;
            case 'gdrive':
                return videoId ? `https://drive.google.com/uc?export=download&id=${videoId}` : null;
            case 'dropbox':
                return url.includes('?dl=0') ? url.replace('?dl=0', '?dl=1') : url;
            case 'direct':
                return url;
            default:
                return null;
        }
    }
    
    // Extraer ID de video de la URL
    extractVideoId(url, platform) {
        const patterns = {
            youtube: [
                /(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/,
                /youtube\.com\/embed\/([a-zA-Z0-9_-]{11})/
            ],
            vimeo: [
                /vimeo\.com\/(?:video\/)?(\d+)/,
                /player\.vimeo\.com\/video\/(\d+)/
            ],
            gdrive: [
                /drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)/,
                /drive\.google\.com\/open\?id=([a-zA-Z0-9_-]+)/
            ]
        };
        
        const platformPatterns = patterns[platform];
        if (!platformPatterns) return null;
        
        for (const pattern of platformPatterns) {
            const match = url.match(pattern);
            if (match) return match[1];
        }
        
        return null;
    }
    
    // Manejo de errores de video
    setupVideoErrorHandling() {
        document.addEventListener('error', (event) => {
            if (event.target.tagName === 'VIDEO' || event.target.tagName === 'IFRAME') {
                const container = event.target.closest('.video-container');
                if (container) {
                    this.handleVideoError(container, container.dataset.videoUrl, container.dataset.platform);
                }
            }
        }, true);
    }
    
    // Manejar error de video
    handleVideoError(container, videoUrl, platform) {
        container.classList.remove('video-loading');
        container.innerHTML = `
            <div class="video-error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>No se pudo cargar el video</p>
                <a href="${videoUrl}" target="_blank" class="video-original-link">
                    <i class="fas fa-external-link-alt"></i>
                    Ver en fuente original
                </a>
            </div>
        `;
    }
    
    // Precargar thumbnails de video
    preloadVideoThumbnails() {
        const thumbnails = document.querySelectorAll('[data-video-thumbnail]');
        thumbnails.forEach(thumb => {
            const img = new Image();
            img.src = thumb.dataset.videoThumbnail;
            img.onload = () => {
                thumb.style.backgroundImage = `url(${thumb.dataset.videoThumbnail})`;
                thumb.classList.add('thumbnail-loaded');
            };
        });
    }
    
    // Analytics básico de videos
    setupVideoAnalytics() {
        document.addEventListener('click', (event) => {
            const videoContainer = event.target.closest('.video-container, .card-video-preview');
            if (videoContainer) {
                const platform = videoContainer.dataset.platform;
                const videoUrl = videoContainer.dataset.videoUrl || 
                               videoContainer.closest('.noticia-card')?.querySelector('[href]')?.href;
                
                // Enviar evento de analytics (si se implementa)
                this.trackVideoInteraction('click', platform, videoUrl);
            }
        });
    }
    
    // Tracking de interacciones con video (placeholder para analytics)
    trackVideoInteraction(action, platform, videoUrl) {
        // Aquí se puede integrar con Google Analytics, etc.
        console.log('Video interaction:', { action, platform, videoUrl });
        
        // Ejemplo de integración con Google Analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'video_interaction', {
                'event_category': 'Video',
                'event_label': platform,
                'value': 1
            });
        }
    }
}

// Integración con el sistema existente
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar VideoManager después del NoticiasManager
    setTimeout(() => {
        window.videoManager = new VideoManager();
        console.log('🎬 Sistema de videos universal inicializado');
    }, 100);
});