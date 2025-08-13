from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime
import json
import math
from .models import Project


class HomeView(TemplateView):
    """Vista principal de la página de inicio de INGLAT"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener proyectos destacados para mostrar en el home
        featured_projects = Project.objects.filter(
            is_featured=True, 
            is_active=True
        ).order_by('-date_completed')[:6]  # Máximo 6 proyectos destacados
        
        # Obtener noticias destacadas para mostrar en el home
        try:
            from apps.blog.models import Noticia
            noticias_destacadas = Noticia.objects.filter(
                destacada=True,
                activa=True
            ).select_related('categoria').order_by('-fecha_publicacion')[:3]
        except ImportError:
            # Si el modelo no existe aún, continuar sin noticias
            noticias_destacadas = []
        
        context.update({
            'current_year': datetime.now().year,
            'page_title': 'INGLAT - Líderes en Energía Renovable',
            'meta_description': 'INGLAT es líder en instalaciones de energía fotovoltaica y renovable. Especialistas en paneles solares, mantenimiento y monitorización en tiempo real.',
            'hero_title': 'Liderando la Transición Energética con Instalaciones Solares Inteligentes',
            'hero_subtitle': 'Monitorización avanzada, control total y soluciones a medida para tu independencia energética.',
            'featured_projects': featured_projects,
            'noticias_destacadas': noticias_destacadas,
        })
        return context



class AboutView(TemplateView):
    """Vista de la página Nosotros"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_year': datetime.now().year,
            'page_title': 'Nosotros - INGLAT',
            'meta_description': 'Conoce más sobre INGLAT, empresa líder en instalaciones de energía renovable con años de experiencia en el sector fotovoltaico.',
        })
        return context


class ServicesView(TemplateView):
    """Vista de la página de Servicios"""
    template_name = 'core/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_year': datetime.now().year,
            'page_title': 'Servicios - INGLAT',
            'meta_description': 'Descubre nuestros servicios: instalación solar, mantenimiento, monitorización y consultoría energética. Soluciones integrales en energía renovable.',
        })
        return context


@method_decorator(csrf_exempt, name='dispatch')
class SimuladorSolarView(TemplateView):
    """Vista del Simulador Solar de INGLAT"""
    template_name = 'core/simulador.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_year': datetime.now().year,
            'page_title': 'Simulador Solar - INGLAT',
            'meta_description': 'Calcula el ahorro y retorno de inversión de tu instalación solar con nuestro simulador avanzado. Resultados personalizados instantáneos.',
        })
        return context
    
    def post(self, request, *args, **kwargs):
        """Procesa los datos del formulario del simulador y calcula resultados"""
        try:
            data = json.loads(request.body)
            
            # Validar y extraer datos del formulario con validaciones robustas
            try:
                consumo_anual = float(data.get('consumo_anual', 0))
                if consumo_anual < 0 or consumo_anual > 100000:
                    raise ValueError("Consumo anual debe estar entre 0 y 100,000 kWh")
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'error': 'Consumo anual inválido'}, status=400)
            
            try:
                superficie = float(data.get('superficie', 0))
                if superficie < 0 or superficie > 10000:
                    raise ValueError("Superficie debe estar entre 0 y 10,000 m²")
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'error': 'Superficie inválida'}, status=400)
            
            try:
                inclinacion = float(data.get('inclinacion', 30))
                if inclinacion < 0 or inclinacion > 90:
                    raise ValueError("Inclinación debe estar entre 0 y 90 grados")
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'error': 'Inclinación inválida'}, status=400)
            
            # Variables booleanas y de texto
            coche_electrico = bool(data.get('coche_electrico', False))
            bateria = bool(data.get('bateria', False))
            ubicacion = str(data.get('ubicacion', '')).strip()
            orientacion = str(data.get('orientacion', 'S')).strip()
            tipo_tejado = str(data.get('tipo_tejado', 'dos_aguas')).strip()
            
            # Validar ubicación no vacía
            if not ubicacion:
                return JsonResponse({'success': False, 'error': 'Ubicación es requerida'}, status=400)
            
            # Realizar cálculos
            resultados = self.calcular_simulacion(
                consumo_anual, coche_electrico, bateria, 
                ubicacion, orientacion, inclinacion, superficie, tipo_tejado
            )
            
            return JsonResponse({
                'success': True,
                'resultados': resultados
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    def calcular_simulacion(self, consumo_anual, coche_electrico, bateria, ubicacion, orientacion, inclinacion, superficie, tipo_tejado=None):
        """Calcula los resultados de la simulación solar usando parámetros configurables"""
        
        # Importar modelos necesarios
        from .models import (
            SimuladorConfig, CostoInstalacion, FactorUbicacion, 
            FactorOrientacion, TipoTejado, AnguloTejado
        )
        
        # Obtener configuración activa
        config = SimuladorConfig.get_activa()
        
        # Parámetros base desde configuración
        horas_sol_promedio = config.horas_sol_promedio
        eficiencia_panel = config.eficiencia_panel
        potencia_panel = config.potencia_panel
        precio_kwh = config.precio_kwh
        
        # Consumo adicional por coche eléctrico
        if coche_electrico:
            consumo_anual += config.consumo_coche_electrico
        
        # Obtener factores desde base de datos
        factor_ubicacion = FactorUbicacion.get_factor_provincia(ubicacion)
        factor_orientacion = FactorOrientacion.get_factor_orientacion(orientacion)
        
        # Factor de inclinación - buscar en base de datos o calcular
        try:
            angulo_tejado = AnguloTejado.objects.get(angulo=int(inclinacion), activo=True)
            factor_inclinacion = angulo_tejado.get_factor_inclinacion()
        except AnguloTejado.DoesNotExist:
            # Cálculo por defecto si no está en BD
            factor_inclinacion = 1.0 - abs(inclinacion - 32) * 0.01
            factor_inclinacion = max(0.7, min(1.0, factor_inclinacion))
        
        # Factor de complejidad del tejado
        factor_complejidad_tejado = 1.0
        if tipo_tejado:
            try:
                tejado = TipoTejado.objects.get(tipo=tipo_tejado, activo=True)
                factor_complejidad_tejado = tejado.factor_complejidad
            except TipoTejado.DoesNotExist:
                pass
        
        # Producción diaria requerida
        produccion_diaria_requerida = consumo_anual / 365
        
        # Potencia instalada necesaria (kW)
        potencia_necesaria = produccion_diaria_requerida / (
            horas_sol_promedio * factor_ubicacion * factor_orientacion * factor_inclinacion
        )
        
        # Limitar por superficie disponible
        paneles_maximos = int(superficie / 2)  # Aprox 2m² por panel
        potencia_maxima_superficie = paneles_maximos * (potencia_panel / 1000)
        potencia_instalada = min(potencia_necesaria, potencia_maxima_superficie)
        
        # Número de paneles
        num_paneles = int(potencia_instalada * 1000 / potencia_panel)
        
        # Producción anual estimada
        produccion_anual = (
            potencia_instalada * 
            horas_sol_promedio * 365 * 
            factor_ubicacion * 
            factor_orientacion * 
            factor_inclinacion
        )
        
        # Autoconsumo (% de la producción que se consume directamente)
        if bateria:
            autoconsumo_porcentaje = config.autoconsumo_con_bateria
            # Obtener costo de batería desde configuración
            costo_instalacion_info = CostoInstalacion.get_costo_para_potencia(potencia_instalada)
            costo_bateria = potencia_instalada * (costo_instalacion_info.costo_bateria_por_kw if costo_instalacion_info else 650)
        else:
            autoconsumo_porcentaje = config.autoconsumo_sin_bateria
            costo_bateria = 0
        
        energia_autoconsumida = produccion_anual * autoconsumo_porcentaje
        energia_excedente = produccion_anual - energia_autoconsumida
        
        # Ahorro anual
        ahorro_autoconsumo = min(energia_autoconsumida, consumo_anual) * precio_kwh
        # Compensación por excedentes
        compensacion_excedentes = energia_excedente * precio_kwh * config.compensacion_excedentes
        ahorro_total_anual = ahorro_autoconsumo + compensacion_excedentes
        
        # Costo total de la instalación (incluyendo factor de complejidad del tejado)
        costo_instalacion_info = CostoInstalacion.get_costo_para_potencia(potencia_instalada)
        costo_base_por_kw = costo_instalacion_info.costo_por_kw if costo_instalacion_info else 1200
        costo_instalacion = (potencia_instalada * costo_base_por_kw * factor_complejidad_tejado) + costo_bateria
        
        # Período de retorno (payback)
        if ahorro_total_anual > 0:
            periodo_retorno = costo_instalacion / ahorro_total_anual
        else:
            periodo_retorno = 0
        
        # Ahorro acumulado en 25 años
        ahorro_25_anos = ahorro_total_anual * 25 - costo_instalacion
        
        # Datos para gráfico año por año
        datos_anuales = []
        ahorro_acumulado = -costo_instalacion
        
        for ano in range(26):  # 0 a 25 años
            if ano == 0:
                ahorro_acumulado = -costo_instalacion
            else:
                # Degradación anual desde configuración
                factor_degradacion = (1 - config.degradacion_anual) ** (ano - 1)
                ahorro_ano = ahorro_total_anual * factor_degradacion
                ahorro_acumulado += ahorro_ano
            
            datos_anuales.append({
                'ano': ano,
                'ahorro_acumulado': round(ahorro_acumulado, 2)
            })
        
        return {
            'potencia_instalada': round(potencia_instalada, 2),
            'num_paneles': num_paneles,
            'superficie_necesaria': round(num_paneles * 2, 2),
            'produccion_anual': round(produccion_anual, 2),
            'autoconsumo_porcentaje': round(autoconsumo_porcentaje * 100, 1),
            'energia_autoconsumida': round(energia_autoconsumida, 2),
            'ahorro_total_anual': round(ahorro_total_anual, 2),
            'costo_instalacion': round(costo_instalacion, 2),
            'periodo_retorno': round(periodo_retorno, 1),
            'ahorro_25_anos': round(ahorro_25_anos, 2),
            'datos_anuales': datos_anuales,
            'incluye_bateria': bateria,
            'costo_bateria': round(costo_bateria, 2),
            'factor_ubicacion': factor_ubicacion,
            'factor_orientacion': factor_orientacion,
            'factor_inclinacion': round(factor_inclinacion, 3),
            'factor_complejidad_tejado': factor_complejidad_tejado
        }