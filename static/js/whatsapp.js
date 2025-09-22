/**
 * WhatsApp Intelligent Integration for INGLAT
 * Handles device detection and appropriate WhatsApp opening mechanism
 */

(function() {
    'use strict';

    // Configuration - loaded dynamically from server
    let config = {
        phoneNumber: '541167214369', // fallback
        defaultMessage: 'Hola, me interesa obtener más información sobre sus servicios.', // fallback
        fallbackUrl: 'https://wa.me/541167214369', // fallback
        debug: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
        loaded: false
    };

    // Configuration loader
    const ConfigLoader = {
        loadConfig: async function() {
            try {
                const response = await fetch('/api/whatsapp-config/', {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    }
                });
                
                if (response.ok) {
                    const serverConfig = await response.json();
                    config.phoneNumber = serverConfig.phoneNumber;
                    config.defaultMessage = serverConfig.defaultMessage;
                    config.fallbackUrl = serverConfig.fallbackUrl;
                    config.loaded = true;
                    
                    if (config.debug) {
                        console.log('WhatsApp config loaded from server:', serverConfig);
                    }
                } else {
                    console.warn('Failed to load WhatsApp config, using fallbacks');
                }
            } catch (error) {
                console.warn('Error loading WhatsApp config:', error);
            }
        }
    };

    // Device detection utilities
    const DeviceDetector = {
        isMobile: function() {
            return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        },
        
        isIOS: function() {
            return /iPad|iPhone|iPod/.test(navigator.userAgent);
        },
        
        isAndroid: function() {
            return /Android/.test(navigator.userAgent);
        },
        
        supportsWhatsAppScheme: function() {
            return this.isMobile();
        },
        
        getDeviceInfo: function() {
            return {
                isMobile: this.isMobile(),
                isIOS: this.isIOS(),
                isAndroid: this.isAndroid(),
                supportsScheme: this.supportsWhatsAppScheme(),
                userAgent: navigator.userAgent
            };
        }
    };

    // WhatsApp URL builders
    const URLBuilder = {
        formatMessage: function(message) {
            return encodeURIComponent(message);
        },
        
        buildWhatsAppUrl: function(useScheme = false) {
            const message = this.formatMessage(config.defaultMessage);
            
            if (useScheme && DeviceDetector.supportsWhatsAppScheme()) {
                // Direct WhatsApp app opening for mobile devices
                return `whatsapp://send?phone=${config.phoneNumber}&text=${message}`;
            } else {
                // WhatsApp Web for desktop or fallback
                return `https://web.whatsapp.com/send?phone=${config.phoneNumber}&text=${message}`;
            }
        },
        
        buildFallbackUrl: function() {
            const message = this.formatMessage(config.defaultMessage);
            return `${config.fallbackUrl}?text=${message}`;
        }
    };

    // Analytics and tracking (optional)
    const Analytics = {
        track: function(event, data = {}) {
            if (config.debug) {
                console.log('WhatsApp Analytics:', event, data);
            }
            
            // Google Analytics tracking if available
            if (typeof gtag !== 'undefined') {
                gtag('event', 'whatsapp_click', {
                    event_category: 'contact',
                    event_label: event,
                    custom_map: data
                });
            }
            
            // Custom analytics can be added here
        }
    };

    // Main WhatsApp handler
    const WhatsAppHandler = {
        init: async function() {
            // Load configuration from server first
            await ConfigLoader.loadConfig();
            
            this.bindEvents();
            if (config.debug) {
                console.log('WhatsApp Handler initialized:', DeviceDetector.getDeviceInfo());
                console.log('Current config:', config);
            }
        },
        
        bindEvents: function() {
            const whatsappButton = document.getElementById('whatsapp-button');
            if (!whatsappButton) {
                console.warn('WhatsApp button not found');
                return;
            }
            
            // Remove default href click behavior and handle custom logic
            whatsappButton.addEventListener('click', this.handleClick.bind(this));
        },
        
        handleClick: function(event) {
            event.preventDefault();
            
            const deviceInfo = DeviceDetector.getDeviceInfo();
            let targetUrl;
            let openMethod = 'fallback';
            
            try {
                if (deviceInfo.isMobile) {
                    // Try to open WhatsApp app first on mobile
                    targetUrl = URLBuilder.buildWhatsAppUrl(true);
                    openMethod = 'app_scheme';
                    
                    // Create temporary iframe to test if WhatsApp app is available
                    const iframe = document.createElement('iframe');
                    iframe.style.display = 'none';
                    iframe.src = targetUrl;
                    document.body.appendChild(iframe);
                    
                    // Fallback to web version after short delay if app doesn't open
                    setTimeout(() => {
                        if (document.body.contains(iframe)) {
                            document.body.removeChild(iframe);
                            // If still here, app probably didn't open, try web version
                            this.openWhatsAppWeb();
                        }
                    }, 1000);
                    
                } else {
                    // Desktop: open WhatsApp Web directly
                    this.openWhatsAppWeb();
                    openMethod = 'web';
                }
                
                // Track the interaction
                Analytics.track('click', {
                    method: openMethod,
                    device: deviceInfo.isMobile ? 'mobile' : 'desktop',
                    url: targetUrl
                });
                
            } catch (error) {
                console.error('Error opening WhatsApp:', error);
                this.openFallback();
                Analytics.track('error', { error: error.message });
            }
        },
        
        openWhatsAppWeb: function() {
            const url = URLBuilder.buildWhatsAppUrl(false);
            window.open(url, '_blank', 'noopener,noreferrer');
        },
        
        openFallback: function() {
            const url = URLBuilder.buildFallbackUrl();
            window.open(url, '_blank', 'noopener,noreferrer');
        }
    };

    // Performance monitoring
    const Performance = {
        measureClickToOpen: function() {
            const startTime = performance.now();
            
            return function() {
                const endTime = performance.now();
                const duration = endTime - startTime;
                
                if (config.debug) {
                    console.log(`WhatsApp open time: ${duration.toFixed(2)}ms`);
                }
                
                return duration;
            };
        }
    };

    // Enhanced button interactions
    const ButtonEnhancer = {
        init: function() {
            const button = document.getElementById('whatsapp-button');
            if (!button) return;
            
            this.addClickFeedback(button);
            this.addLoadingState(button);
        },
        
        addClickFeedback: function(button) {
            button.addEventListener('mousedown', function() {
                this.style.transform = 'scale(0.95)';
            });
            
            button.addEventListener('mouseup', function() {
                this.style.transform = '';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        },
        
        addLoadingState: function(button) {
            button.addEventListener('click', function() {
                const originalHTML = this.innerHTML;
                this.style.pointerEvents = 'none';
                
                // Brief loading state
                setTimeout(() => {
                    this.innerHTML = originalHTML;
                    this.style.pointerEvents = '';
                }, 800);
            });
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', async function() {
            await WhatsAppHandler.init();
            ButtonEnhancer.init();
        });
    } else {
        (async () => {
            await WhatsAppHandler.init();
            ButtonEnhancer.init();
        })();
    }

    // Expose for debugging in development
    if (config.debug) {
        window.WhatsAppDebug = {
            config,
            DeviceDetector,
            URLBuilder,
            Analytics,
            WhatsAppHandler
        };
    }

})();