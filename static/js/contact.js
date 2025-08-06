/**
 * CONTACT.JS - JavaScript para la p�gina de contacto
 * Funcionalidades: validaci�n del formulario, env�o AJAX, UX mejorada
 */

document.addEventListener('DOMContentLoaded', function() {
    initContactForm();
    initSmoothScrolling();
    initFormEnhancements();
});

/**
 * Inicializar el formulario de contacto
 */
function initContactForm() {
    const form = document.getElementById('contact-form');
    const submitButton = document.getElementById('submit-button');
    
    if (!form || !submitButton) return;
    
    // Manejar el env�o del formulario
    form.addEventListener('submit', handleFormSubmit);
    
    // Validaci�n en tiempo real
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', () => validateField(input));
        input.addEventListener('input', () => clearFieldError(input));
    });
    
    // Mejorar la experiencia del tipo de proyecto
    const tipoProyectoSelect = form.querySelector('#id_tipo_proyecto');
    if (tipoProyectoSelect) {
        enhanceProjectTypeSelect(tipoProyectoSelect);
    }
}

/**
 * Manejar el env�o del formulario (AJAX)
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = document.getElementById('submit-button');
    const submitText = submitButton.querySelector('.submit-text');
    const loadingText = submitButton.querySelector('.loading-text');
    
    // Validar formulario antes del env�o
    if (!validateForm(form)) {
        showMessage('Por favor, corrige los errores en el formulario.', 'error');
        return;
    }
    
    // Cambiar estado del bot�n
    setButtonLoading(submitButton, true);
    
    try {
        const formData = new FormData(form);
        
        const response = await fetch(form.action || window.location.pathname, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCsrfToken()
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // �xito - redirigir o mostrar mensaje
            showMessage(data.message || '�Mensaje enviado correctamente!', 'success');
            form.reset();
            
            // Redirigir despu�s de un breve delay
            setTimeout(() => {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                } else {
                    window.location.href = '/contacto/enviado/';
                }
            }, 2000);
            
        } else {
            // Errores del formulario
            if (data.errors) {
                displayFormErrors(form, data.errors);
            }
            showMessage(data.message || 'Hay errores en el formulario.', 'error');
        }
        
    } catch (error) {
        console.error('Error al enviar el formulario:', error);
        showMessage('Hubo un problema al enviar el formulario. Por favor, int�ntalo de nuevo.', 'error');
    } finally {
        setButtonLoading(submitButton, false);
    }
}

/**
 * Validar formulario completo
 */
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Validar un campo individual
 */
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';
    
    // Limpiar errores previos
    clearFieldError(field);
    
    // Validaci�n de campos requeridos
    if (field.hasAttribute('required') && !value) {
        errorMessage = 'Este campo es obligatorio.';
        isValid = false;
    }
    
    // Validaciones espec�ficas por tipo de campo
    if (value && isValid) {
        switch (fieldName) {
            case 'nombre':
                if (value.length < 2) {
                    errorMessage = 'El nombre debe tener al menos 2 caracteres.';
                    isValid = false;
                } else if (!/^[a-zA-Z������������\s]+$/.test(value)) {
                    errorMessage = 'El nombre solo debe contener letras y espacios.';
                    isValid = false;
                }
                break;
                
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(value)) {
                    errorMessage = 'Por favor, introduce un email v�lido.';
                    isValid = false;
                }
                break;
                
            case 'telefono':
                if (value) {
                    const phoneRegex = /^[\+]?[0-9\s\-\(\)]{9,15}$/;
                    if (!phoneRegex.test(value)) {
                        errorMessage = 'Por favor, introduce un tel�fono v�lido.';
                        isValid = false;
                    }
                }
                break;
                
            case 'mensaje':
                if (value.length < 10) {
                    errorMessage = 'El mensaje debe tener al menos 10 caracteres.';
                    isValid = false;
                } else if (value.length > 1000) {
                    errorMessage = 'El mensaje no puede exceder los 1000 caracteres.';
                    isValid = false;
                }
                break;
        }
    }
    
    // Mostrar error si existe
    if (!isValid) {
        showFieldError(field, errorMessage);
    }
    
    return isValid;
}

/**
 * Mostrar error en un campo espec�fico
 */
function showFieldError(field, message) {
    const formGroup = field.closest('.form-group');
    if (!formGroup) return;
    
    // Buscar error existente
    let errorElement = formGroup.querySelector('.form-error');
    
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'form-error';
        formGroup.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
    field.classList.add('field-error');
}

/**
 * Limpiar error de un campo
 */
function clearFieldError(field) {
    const formGroup = field.closest('.form-group');
    if (!formGroup) return;
    
    const errorElement = formGroup.querySelector('.form-error');
    if (errorElement) {
        errorElement.remove();
    }
    
    field.classList.remove('field-error');
}

/**
 * Mostrar errores del formulario desde el servidor
 */
function displayFormErrors(form, errors) {
    // Limpiar errores previos
    form.querySelectorAll('.form-error').forEach(error => error.remove());
    form.querySelectorAll('.field-error').forEach(field => field.classList.remove('field-error'));
    
    // Mostrar nuevos errores
    Object.keys(errors).forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (field && errors[fieldName].length > 0) {
            showFieldError(field, errors[fieldName][0]);
        }
    });
}

/**
 * Cambiar estado de carga del bot�n
 */
function setButtonLoading(button, isLoading) {
    const submitText = button.querySelector('.submit-text');
    const loadingText = button.querySelector('.loading-text');
    
    if (isLoading) {
        button.disabled = true;
        submitText.style.display = 'none';
        loadingText.style.display = 'inline-flex';
    } else {
        button.disabled = false;
        submitText.style.display = 'inline';
        loadingText.style.display = 'none';
    }
}

/**
 * Mostrar mensaje de feedback
 */
function showMessage(message, type = 'info') {
    // Buscar o crear contenedor de mensajes
    let messageContainer = document.querySelector('.alert-container');
    
    if (!messageContainer) {
        messageContainer = document.createElement('div');
        messageContainer.className = 'alert-container';
        
        // Insertar despu�s del t�tulo de la tarjeta
        const cardTitle = document.querySelector('.card__title');
        if (cardTitle) {
            cardTitle.parentNode.insertBefore(messageContainer, cardTitle.nextSibling);
        }
    }
    
    // Crear mensaje
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert--${type}`;
    
    const icon = type === 'success' ? 'check-circle' : 
                 type === 'error' ? 'exclamation-triangle' : 'info-circle';
    
    alertDiv.innerHTML = `
        <i class="fas fa-${icon}"></i>
        ${message}
    `;
    
    // Limpiar mensajes anteriores y agregar nuevo
    messageContainer.innerHTML = '';
    messageContainer.appendChild(alertDiv);
    
    // Scroll al mensaje
    alertDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Auto-ocultar despu�s de 5 segundos para mensajes de �xito
    if (type === 'success') {
        setTimeout(() => {
            alertDiv.style.transition = 'opacity 0.5s ease';
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 500);
        }, 5000);
    }
}

/**
 * Mejorar el select de tipo de proyecto
 */
function enhanceProjectTypeSelect(select) {
    select.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        
        // A�adir efecto visual al seleccionar
        this.style.borderColor = 'var(--primary-color)';
        this.style.boxShadow = '0 0 0 3px rgba(0, 100, 102, 0.1)';
        
        setTimeout(() => {
            this.style.borderColor = '';
            this.style.boxShadow = '';
        }, 1000);
    });
}

/**
 * Inicializar scroll suave para enlaces internos
 */
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
}

/**
 * Inicializar mejoras adicionales del formulario
 */
function initFormEnhancements() {
    // Contador de caracteres para el mensaje
    const messageTextarea = document.querySelector('#id_mensaje');
    if (messageTextarea) {
        addCharacterCounter(messageTextarea, 1000);
    }
    
    // Mejorar campos de tel�fono
    const phoneInput = document.querySelector('#id_telefono');
    if (phoneInput) {
        formatPhoneInput(phoneInput);
    }
}

/**
 * A�adir contador de caracteres
 */
function addCharacterCounter(textarea, maxLength) {
    const formGroup = textarea.closest('.form-group');
    const counter = document.createElement('div');
    counter.className = 'character-counter';
    counter.style.cssText = `
        font-size: var(--text-sm);
        color: var(--gray-500);
        text-align: right;
        margin-top: var(--space-1);
    `;
    
    function updateCounter() {
        const remaining = maxLength - textarea.value.length;
        counter.textContent = `${textarea.value.length}/${maxLength} caracteres`;
        
        if (remaining < 100) {
            counter.style.color = remaining < 0 ? 'var(--error)' : 'var(--warning)';
        } else {
            counter.style.color = 'var(--gray-500)';
        }
    }
    
    textarea.addEventListener('input', updateCounter);
    formGroup.appendChild(counter);
    updateCounter(); // Inicializar
}

/**
 * Formatear input de tel�fono
 */
function formatPhoneInput(input) {
    input.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, ''); // Solo n�meros
        
        // Formato espa�ol
        if (value.length >= 9) {
            if (value.startsWith('34')) {
                value = '+34 ' + value.slice(2, 5) + ' ' + value.slice(5, 8) + ' ' + value.slice(8, 11);
            } else if (value.length === 9) {
                value = value.slice(0, 3) + ' ' + value.slice(3, 6) + ' ' + value.slice(6, 9);
            }
        }
        
        e.target.value = value;
    });
}

/**
 * Obtener token CSRF
 */
function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}

/**
 * Utilidades para integraci�n con WhatsApp
 */
window.contactUtils = {
    /**
     * Abrir WhatsApp con mensaje preconfigurado basado en el tipo de proyecto
     */
    openWhatsAppWithProject: function(projectType = '') {
        const baseNumber = '541167214369'; // Reemplazar con n�mero real
        let message = 'Hola INGLAT, me interesa conocer m�s sobre las instalaciones solares.';
        
        if (projectType) {
            const projectNames = {
                'residencial': 'instalaciones residenciales',
                'comercial': 'instalaciones comerciales',
                'industrial': 'instalaciones industriales',
                'autoconsumo': 'sistemas de autoconsumo',
                'baterias': 'sistemas con bater�as',
                'mantenimiento': 'servicios de mantenimiento',
                'consultoria': 'consultor�a energ�tica'
            };
            
            if (projectNames[projectType]) {
                message = `Hola INGLAT, me interesa conocer m�s sobre ${projectNames[projectType]}.`;
            }
        }
        
        const whatsappUrl = `https://wa.me/${baseNumber}?text=${encodeURIComponent(message)}`;
        window.open(whatsappUrl, '_blank');
    },
    
    /**
     * Obtener datos del formulario para WhatsApp
     */
    getFormDataForWhatsApp: function() {
        const form = document.getElementById('contact-form');
        if (!form) return '';
        
        const formData = new FormData(form);
        const data = {
            nombre: formData.get('nombre'),
            email: formData.get('email'),
            telefono: formData.get('telefono'),
            tipo_proyecto: formData.get('tipo_proyecto'),
            mensaje: formData.get('mensaje')
        };
        
        let message = 'Hola INGLAT, he completado el formulario de contacto con esta informaci�n:\n\n';
        message += `Nombre: ${data.nombre}\n`;
        message += `Email: ${data.email}\n`;
        if (data.telefono) message += `Tel�fono: ${data.telefono}\n`;
        message += `Tipo de proyecto: ${data.tipo_proyecto}\n`;
        message += `Mensaje: ${data.mensaje}`;
        
        return message;
    }
};

// A�adir estilos para errores de campo
const style = document.createElement('style');
style.textContent = `
    .field-error {
        border-color: var(--error) !important;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
    }
    
    .character-counter {
        transition: color 0.3s ease;
    }
    
    .alert-container {
        margin: var(--space-4) 0;
    }
`;
document.head.appendChild(style);