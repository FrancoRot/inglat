// simulador.js - Funcionalidad del Simulador Solar INGLAT

class SimuladorSolar {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 5;
        this.formData = {};
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.updateNavigation();
        this.initializeFormElements();
    }
    
    bindEvents() {
        // Navegación del wizard
        document.getElementById('prev-btn').addEventListener('click', () => this.prevStep());
        document.getElementById('next-btn').addEventListener('click', () => this.nextStep());
        
        // Submit del formulario
        document.getElementById('simulador-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.processSimulation();
        });
        
        // Calculadora de consumo
        document.getElementById('calcular-consumo').addEventListener('click', () => this.calcularConsumoEstimado());
        
        // Visual feedback para preferencias
        this.addPreferenceAnimations();
        
        // Visual feedback para selecciones de tejado
        this.addRoofSelectionAnimations();
        
        // Validaciones en tiempo real
        this.addRealtimeValidation();
    }
    
    initializeFormElements() {
        // Inicializar elementos del formulario con valores por defecto
        this.initializeDefaultValues();
    }
    
    addRealtimeValidation() {
        // Validación del consumo anual
        const consumoInput = document.getElementById('consumo_anual');
        if (consumoInput) {
            consumoInput.addEventListener('input', (e) => {
                const value = parseFloat(e.target.value);
                const helpText = e.target.nextElementSibling;
                
                if (value < 500) {
                    helpText.textContent = 'Consumo muy bajo. Verifica si es correcto.';
                    helpText.style.color = 'var(--warning)';
                } else if (value > 20000) {
                    helpText.textContent = 'Consumo muy alto. ¿Es para uso comercial o industrial?';
                    helpText.style.color = 'var(--warning)';
                } else {
                    helpText.textContent = 'Consumo típico: Vivienda pequeña (2000-3000 kWh), Media (3000-5000 kWh), Grande (5000+ kWh)';
                    helpText.style.color = 'var(--gray-500)';
                }
            });
        }
        
        // Validación de superficie
        const superficieInput = document.getElementById('superficie');
        if (superficieInput) {
            superficieInput.addEventListener('input', (e) => {
                const value = parseFloat(e.target.value);
                const helpText = e.target.nextElementSibling;
                const panelesPosibles = Math.floor(value / 2);
                
                if (value < 20) {
                    helpText.textContent = 'Superficie pequeña. Podrías tener limitaciones en la potencia instalable.';
                    helpText.style.color = 'var(--warning)';
                } else {
                    helpText.textContent = `Cada panel solar ocupa aproximadamente 2m². Con ${value}m² podrías instalar ~${panelesPosibles} paneles.`;
                    helpText.style.color = 'var(--gray-500)';
                }
            });
        }
    }
    
    calcularConsumoEstimado() {
        const habitantes = document.getElementById('habitantes').value;
        const tipoVivienda = document.getElementById('tipo_vivienda').value;
        
        if (!habitantes || !tipoVivienda) {
            alert('Por favor, selecciona el número de habitantes y tipo de vivienda.');
            return;
        }
        
        // Tabla de consumos estimados (kWh/año)
        const consumosPorHabitante = {
            'piso': { '1': 1800, '2': 2500, '3': 3200, '4': 3800, '5': 4500 },
            'casa': { '1': 2200, '2': 3000, '3': 3800, '4': 4500, '5': 5500 },
            'chalet': { '1': 2800, '2': 3800, '3': 4800, '4': 5800, '5': 7000 }
        };
        
        const consumoEstimado = consumosPorHabitante[tipoVivienda][habitantes] || 4000;
        
        // Actualizar el campo de consumo
        document.getElementById('consumo_anual').value = consumoEstimado;
        
        // Mostrar mensaje de confirmación
        this.showNotification(`Consumo estimado calculado: ${consumoEstimado.toLocaleString()} kWh/año`, 'success');
    }
    
    initializeDefaultValues() {
        // Establecer valores por defecto si no están seleccionados
        const orientacionNorte = document.querySelector('input[name="orientacion"][value="N"]');
        if (orientacionNorte && !document.querySelector('input[name="orientacion"]:checked')) {
            orientacionNorte.checked = true;
        }
        
        const tejadoDosAguas = document.querySelector('input[name="tipo_tejado"][value="dos_aguas"]');
        if (tejadoDosAguas && !document.querySelector('input[name="tipo_tejado"]:checked')) {
            tejadoDosAguas.checked = true;
        }
        
        const angulo30 = document.querySelector('input[name="inclinacion"][value="30"]');
        if (angulo30 && !document.querySelector('input[name="inclinacion"]:checked')) {
            angulo30.checked = true;
        }
    }
    
    addPreferenceAnimations() {
        // Animaciones para preferencias con imágenes
        const preferenceCards = document.querySelectorAll('.preference-card');
        
        preferenceCards.forEach(card => {
            const checkbox = card.querySelector('input[type="checkbox"]');
            const image = card.querySelector('.preference-image');
            
            if (checkbox && image) {
                checkbox.addEventListener('change', (e) => {
                    if (e.target.checked) {
                        card.classList.add('selected');
                        image.style.filter = 'brightness(1.1) saturate(1.2)';
                        
                        // Animación de selección
                        card.style.transform = 'scale(1.02)';
                        setTimeout(() => {
                            card.style.transform = 'scale(1)';
                        }, 200);
                    } else {
                        card.classList.remove('selected');
                        image.style.filter = 'none';
                    }
                });
            }
        });
    }
    
    addRoofSelectionAnimations() {
        // Animaciones para selección de tipo de tejado
        this.addRadioGroupAnimations('tipo_tejado', '.roof-type-card');
        
        // Animaciones para selección de ángulo
        this.addRadioGroupAnimations('inclinacion', '.angle-card');
        
        // Animaciones para orientación
        this.addRadioGroupAnimations('orientacion', '.orientation-card');
    }
    
    addRadioGroupAnimations(groupName, cardSelector) {
        const radioButtons = document.querySelectorAll(`input[name="${groupName}"]`);
        
        radioButtons.forEach(radio => {
            radio.addEventListener('change', (e) => {
                // Remover animación de todas las cartas del grupo
                const allCards = document.querySelectorAll(`input[name="${groupName}"] + ${cardSelector}`);
                allCards.forEach(card => {
                    card.style.transform = 'scale(1)';
                    card.style.transition = 'all 0.3s ease';
                });
                
                // Animar carta seleccionada
                if (e.target.checked) {
                    const selectedCard = e.target.nextElementSibling;
                    if (selectedCard) {
                        selectedCard.style.transform = 'scale(1.05)';
                        setTimeout(() => {
                            selectedCard.style.transform = 'scale(1)';
                        }, 300);
                        
                        // Efecto de selección especial para ángulo óptimo
                        if (groupName === 'inclinacion' && e.target.value === '30') {
                            selectedCard.style.boxShadow = '0 0 25px rgba(34, 197, 94, 0.4)';
                            setTimeout(() => {
                                selectedCard.style.boxShadow = '';
                            }, 1500);
                        }
                        
                        // Feedback para orientación óptima
                        if (groupName === 'orientacion' && e.target.value === 'N') {
                            this.showNotification('¡Excelente! La orientación Norte es óptima para Argentina.', 'success');
                        }
                    }
                }
            });
        });
    }
    
    nextStep() {
        if (this.validateCurrentStep()) {
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                this.updateStepDisplay();
                this.updateNavigation();
                
                // Si llegamos al último paso y no es resultados, enviar formulario
                if (this.currentStep === 5) {
                    this.processSimulation();
                }
            }
        }
    }
    
    prevStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateStepDisplay();
            this.updateNavigation();
        }
    }
    
    goToStep(step) {
        if (step >= 1 && step <= this.totalSteps) {
            this.currentStep = step;
            this.updateStepDisplay();
            this.updateNavigation();
        }
    }
    
    validateCurrentStep() {
        const currentStepElement = document.querySelector(`.wizard-step[data-step="${this.currentStep}"]`);
        const requiredInputs = currentStepElement.querySelectorAll('input[required], select[required]');
        
        let isValid = true;
        let errorMessages = [];
        
        requiredInputs.forEach(input => {
            let fieldValid = true;
            
            if (input.type === 'radio') {
                // Para radio buttons, verificar si hay alguno seleccionado del grupo
                const radioGroup = document.querySelector(`input[name="${input.name}"]:checked`);
                if (!radioGroup) {
                    fieldValid = false;
                    if (input.name === 'orientacion') {
                        errorMessages.push('Selecciona la orientación del tejado');
                    } else if (input.name === 'tipo_tejado') {
                        errorMessages.push('Selecciona el tipo de tejado');
                    } else if (input.name === 'inclinacion') {
                        errorMessages.push('Selecciona el ángulo del tejado');
                    }
                }
            } else if (input.type === 'number') {
                // Para campos numéricos, verificar valor y rango
                const value = parseFloat(input.value);
                if (!input.value || isNaN(value) || value <= 0) {
                    fieldValid = false;
                    if (input.id === 'consumo_anual') {
                        errorMessages.push('Ingresa un consumo anual válido');
                    } else if (input.id === 'superficie') {
                        errorMessages.push('Ingresa una superficie disponible válida');
                    }
                }
            } else if (input.tagName === 'SELECT') {
                // Para selects, verificar que tenga un valor seleccionado
                if (!input.value) {
                    fieldValid = false;
                    if (input.id === 'ubicacion') {
                        errorMessages.push('Selecciona tu provincia');
                    }
                }
            } else {
                // Para otros inputs, verificar que no estén vacíos
                if (!input.value.trim()) {
                    fieldValid = false;
                }
            }
            
            if (!fieldValid) {
                isValid = false;
                input.classList.add('error');
                
                // Remover clase de error después de 5 segundos
                setTimeout(() => input.classList.remove('error'), 5000);
            } else {
                input.classList.remove('error');
            }
        });
        
        if (!isValid) {
            const message = errorMessages.length > 0 ? errorMessages[0] : 'Por favor, completa todos los campos requeridos.';
            this.showNotification(message, 'error');
        }
        
        return isValid;
    }
    
    updateStepDisplay() {
        // Ocultar todos los pasos
        document.querySelectorAll('.wizard-step').forEach(step => {
            step.classList.remove('active');
        });
        
        // Mostrar paso actual
        const currentStepElement = document.querySelector(`.wizard-step[data-step="${this.currentStep}"]`);
        if (currentStepElement) {
            currentStepElement.classList.add('active');
        }
        
        // Actualizar indicadores de paso
        document.querySelectorAll('.wizard-steps .step').forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.remove('active', 'completed');
            
            if (stepNumber === this.currentStep) {
                step.classList.add('active');
            } else if (stepNumber < this.currentStep) {
                step.classList.add('completed');
            }
        });
    }
    
    updateNavigation() {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        
        // Botón anterior
        if (this.currentStep === 1) {
            prevBtn.style.display = 'none';
        } else {
            prevBtn.style.display = 'inline-flex';
        }
        
        // Botón siguiente
        if (this.currentStep === this.totalSteps) {
            nextBtn.style.display = 'none';
        } else if (this.currentStep === this.totalSteps - 1) {
            nextBtn.textContent = 'Calcular →';
            nextBtn.style.display = 'inline-flex';
        } else {
            nextBtn.textContent = 'Siguiente →';
            nextBtn.style.display = 'inline-flex';
        }
    }
    
    collectFormData() {
        const formData = {};
        
        // Recopilar datos del formulario
        formData.consumo_anual = parseFloat(document.getElementById('consumo_anual').value) || 0;
        formData.coche_electrico = document.getElementById('coche_electrico').checked;
        formData.bateria = document.getElementById('bateria').checked;
        formData.ubicacion = document.getElementById('ubicacion').value;
        formData.orientacion = document.querySelector('input[name="orientacion"]:checked')?.value || 'N';
        formData.tipo_tejado = document.querySelector('input[name="tipo_tejado"]:checked')?.value || 'dos_aguas';
        formData.inclinacion = parseFloat(document.querySelector('input[name="inclinacion"]:checked')?.value) || 30;
        formData.superficie = parseFloat(document.getElementById('superficie').value) || 0;
        
        return formData;
    }
    
    async processSimulation() {
        const submitBtn = document.querySelector('button[type="submit"]');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');
        
        // Mostrar loading
        btnText.style.display = 'none';
        btnLoader.style.display = 'flex';
        submitBtn.disabled = true;
        
        try {
            const formData = this.collectFormData();
            
            const response = await fetch('/simulador/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayResults(data.resultados, formData);
                // Ir al paso de resultados
                this.currentStep = 5;
                this.updateStepDisplay();
                this.updateNavigation();
            } else {
                this.displayError(data.error || 'Error desconocido en el cálculo');
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.displayError('Error de conexión. Por favor, inténtalo de nuevo.');
        } finally {
            // Ocultar loading
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
            submitBtn.disabled = false;
        }
    }
    
    displayResults(resultados, formData) {
        const container = document.getElementById('resultados-container');
        
        const html = `
            <div class="resultados-content">
                <h3 class="step-heading">Resultados de tu Simulación Solar</h3>
                <p class="step-description">
                    Basado en tus datos, aquí tienes un análisis detallado de tu instalación solar personalizada.
                </p>
                
                <!-- Resumen Principal -->
                <div class="resultados-grid">
                    <div class="resultado-card">
                        <span class="resultado-value">${resultados.potencia_instalada}</span>
                        <span class="resultado-label">kW Instalados</span>
                        <div class="resultado-description">${resultados.num_paneles} paneles solares</div>
                    </div>
                    <div class="resultado-card">
                        <span class="resultado-value">${resultados.produccion_anual.toLocaleString()}</span>
                        <span class="resultado-label">kWh/año</span>
                        <div class="resultado-description">Producción anual estimada</div>
                    </div>
                    <div class="resultado-card">
                        <span class="resultado-value">USD ${resultados.ahorro_total_anual.toLocaleString()}</span>
                        <span class="resultado-label">Ahorro Anual</span>
                        <div class="resultado-description">${resultados.autoconsumo_porcentaje}% autoconsumo</div>
                    </div>
                    <div class="resultado-card">
                        <span class="resultado-value">${resultados.periodo_retorno}</span>
                        <span class="resultado-label">Años</span>
                        <div class="resultado-description">Período de retorno</div>
                    </div>
                </div>
                
                <!-- Gráfico de Ahorro Acumulado -->
                <div class="chart-container">
                    <h4 class="chart-title">Evolución del Ahorro Acumulado en USD (25 años)</h4>
                    <canvas id="ahorroChart" width="400" height="200"></canvas>
                </div>
                
                <!-- Tabla Resumen Detallada -->
                <table class="resumen-table">
                    <thead>
                        <tr>
                            <th>Concepto</th>
                            <th>Valor</th>
                            <th>Descripción</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Inversión Inicial</strong></td>
                            <td>USD ${resultados.costo_instalacion.toLocaleString()}</td>
                            <td>Instalación completa ${resultados.incluye_bateria ? '(incluye batería)' : '(sin batería)'}</td>
                        </tr>
                        <tr>
                            <td>Superficie necesaria</td>
                            <td>${resultados.superficie_necesaria} m²</td>
                            <td>Espacio requerido para ${resultados.num_paneles} paneles</td>
                        </tr>
                        <tr>
                            <td>Producción anual</td>
                            <td>${resultados.produccion_anual.toLocaleString()} kWh</td>
                            <td>Energía generada por año</td>
                        </tr>
                        <tr>
                            <td>Autoconsumo</td>
                            <td>${resultados.autoconsumo_porcentaje}%</td>
                            <td>Porcentaje de energía que consumes directamente</td>
                        </tr>
                        <tr>
                            <td>Ahorro anual</td>
                            <td>USD ${resultados.ahorro_total_anual.toLocaleString()}</td>
                            <td>Reducción en tu factura eléctrica</td>
                        </tr>
                        <tr class="highlight">
                            <td><strong>Ahorro en 25 años</strong></td>
                            <td><strong>USD ${resultados.ahorro_25_anos.toLocaleString()}</strong></td>
                            <td><strong>Beneficio total del sistema</strong></td>
                        </tr>
                    </tbody>
                </table>
                
                <!-- Acciones Finales -->
                <div class="resultados-actions">
                    <div style="text-align: center; margin-top: var(--space-6);">
                        <h4>¿Te interesa esta propuesta?</h4>
                        <p style="color: var(--gray-700); margin-bottom: var(--space-4);">
                            Nuestros expertos pueden refinar estos cálculos y diseñar una solución personalizada para ti.
                        </p>
                        <div class="hero__actions">
                            <a href="/contacto/" class="btn btn--primary">
                                Solicitar Consulta Personalizada
                            </a>
                            <a href="https://wa.me/541167214369?text=Hola,%20he%20usado%20el%20simulador%20solar%20y%20me%20interesa%20más%20información" 
                               class="btn btn--accent" target="_blank">
                                💬 Contactar por WhatsApp
                            </a>
                        </div>
                        <button type="button" class="btn btn--secondary" onclick="window.simulador.resetSimulator()" style="margin-top: var(--space-4);">
                            🔄 Nueva Simulación
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
        container.style.display = 'block';
        
        // Crear gráfico
        this.createChart(resultados.datos_anuales);
        
        // Ocultar contenedor de error si estaba visible
        document.getElementById('error-container').style.display = 'none';
    }
    
    createChart(datosAnuales) {
        const ctx = document.getElementById('ahorroChart').getContext('2d');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: datosAnuales.map(d => `Año ${d.ano}`),
                datasets: [{
                    label: 'Ahorro Acumulado (USD)',
                    data: datosAnuales.map(d => d.ahorro_acumulado),
                    borderColor: 'var(--primary-color)',
                    backgroundColor: 'rgba(0, 100, 102, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'var(--primary-color)',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                aspectRatio: 2,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: 'var(--primary-color)',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Tiempo (años)'
                        },
                        ticks: {
                            maxTicksLimit: 10
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Ahorro Acumulado (USD)'
                        },
                        ticks: {
                            callback: function(value) {
                                return 'USD ' + value.toLocaleString();
                            }
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }
    
    displayError(errorMessage) {
        const errorContainer = document.getElementById('error-container');
        const errorText = document.getElementById('error-text');
        
        errorText.textContent = errorMessage;
        errorContainer.style.display = 'block';
        
        // Ocultar contenedor de resultados si estaba visible
        document.getElementById('resultados-container').style.display = 'none';
        
        // Ir al paso de resultados para mostrar el error
        this.currentStep = 5;
        this.updateStepDisplay();
        this.updateNavigation();
    }
    
    resetSimulator() {
        // Resetear al primer paso
        this.currentStep = 1;
        
        // Limpiar formulario
        document.getElementById('simulador-form').reset();
        
        // Resetear valores por defecto
        this.initializeDefaultValues();
        
        // Actualizar display
        this.updateStepDisplay();
        this.updateNavigation();
        
        // Limpiar resultados
        document.getElementById('resultados-container').style.display = 'none';
        document.getElementById('error-container').style.display = 'none';
        
        // Scroll al inicio
        document.querySelector('.hero').scrollIntoView({ behavior: 'smooth' });
        
        this.showNotification('Simulador reiniciado. Puedes comenzar una nueva simulación.', 'success');
    }
    
    showNotification(message, type = 'info') {
        // Crear notificación temporal
        const notification = document.createElement('div');
        notification.className = `notification notification--${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: var(--space-4);
            background: var(--${type === 'error' ? 'error' : type === 'success' ? 'success' : 'info'});
            color: white;
            border-radius: var(--border-radius);
            z-index: 1000;
            animation: slideInRight 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Remover después de 4 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    }
}

// Función global para ir a un paso específico
function goToStep(step) {
    if (window.simulador) {
        window.simulador.goToStep(step);
    }
}

// Inicializar simulador cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    window.simulador = new SimuladorSolar();
});

// Agregar animaciones CSS para las notificaciones
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .form-input.error {
        border-color: var(--error) !important;
        animation: shake 0.5s ease-in-out;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
`;
document.head.appendChild(notificationStyles);