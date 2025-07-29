# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import TextInput, Textarea
from .models import (
    Project, SimuladorConfig, CostoInstalacion, 
    FactorUbicacion, FactorOrientacion, TipoTejado, AnguloTejado
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Configuracion del panel de administracion para Proyectos"""
    
    list_display = [
        'title', 
        'location', 
        'date_completed', 
        'power_capacity',
        'client_type',
        'is_featured', 
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'is_featured', 
        'is_active',
        'client_type',
        'date_completed',
        'created_at'
    ]
    
    search_fields = [
        'title', 
        'location', 
        'description_short',
        'client_type',
        'power_capacity'
    ]
    
    list_editable = [
        'is_featured', 
        'is_active'
    ]
    
    prepopulated_fields = {
        'slug': ('title',)
    }
    
    fieldsets = (
        ('Informacion Principal', {
            'fields': ('title', 'slug', 'location', 'date_completed')
        }),
        ('Descripcion', {
            'fields': ('description_short', 'description_full')
        }),
        ('Detalles Tecnicos', {
            'fields': ('power_capacity', 'client_type')
        }),
        ('Imagen', {
            'fields': ('featured_image',)
        }),
        ('Configuracion', {
            'fields': ('is_featured', 'is_active'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    ordering = ['-date_completed', '-created_at']
    
    # Configuracion de la vista de lista
    list_per_page = 20
    date_hierarchy = 'date_completed'
    
    # Configuracion de formularios
    save_on_top = True
    
    def get_queryset(self, request):
        """Optimizar las consultas para el listado del admin"""
        return super().get_queryset(request).select_related()
    
    class Media:
        css = {
            'all': ('admin/css/custom-project-admin.css',)
        }
        js = ('admin/js/custom-project-admin.js',)


# ======================================
# ADMIN PARA SIMULADOR SOLAR
# ======================================

@admin.register(SimuladorConfig)
class SimuladorConfigAdmin(admin.ModelAdmin):
    """Administrador para configuración del simulador"""
    
    list_display = [
        'nombre', 
        'activa_display', 
        'precio_kwh', 
        'horas_sol_promedio',
        'eficiencia_panel_display',
        'fecha_actualizacion'
    ]
    
    list_filter = [
        'activa',
        'fecha_creacion'
    ]
    
    search_fields = ['nombre']
    
    fieldsets = [
        ('Información General', {
            'fields': ('nombre', 'activa')
        }),
        ('Parámetros Técnicos', {
            'fields': (
                'horas_sol_promedio', 
                'eficiencia_panel', 
                'potencia_panel',
                'degradacion_anual'
            ),
            'classes': ('wide',)
        }),
        ('Precios y Consumos', {
            'fields': (
                'precio_kwh',
                'consumo_coche_electrico'
            ),
            'classes': ('wide',)
        }),
        ('Factores de Autoconsumo', {
            'fields': (
                'autoconsumo_con_bateria',
                'autoconsumo_sin_bateria',
                'compensacion_excedentes'
            ),
            'classes': ('wide',)
        }),
    ]
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    # Personalizar widgets para mejor UX
    formfield_overrides = {
        models.FloatField: {'widget': TextInput(attrs={'size': '10'})},
        models.IntegerField: {'widget': TextInput(attrs={'size': '10'})},
    }
    
    def activa_display(self, obj):
        if obj.activa:
            return format_html('<span style="color: green; font-weight: bold;">✓ ACTIVA</span>')
        else:
            return format_html('<span style="color: gray;">Inactiva</span>')
    activa_display.short_description = 'Estado'
    
    def eficiencia_panel_display(self, obj):
        return f"{obj.eficiencia_panel * 100:.1f}%"
    eficiencia_panel_display.short_description = 'Eficiencia'
    
    save_on_top = True


@admin.register(CostoInstalacion)
class CostoInstalacionAdmin(admin.ModelAdmin):
    """Administrador para costos de instalación"""
    
    list_display = [
        'rango_potencia_display',
        'costo_por_kw_display',
        'costo_bateria_por_kw_display',
        'activo'
    ]
    
    list_filter = ['activo']
    
    fields = [
        'rango_potencia',
        'potencia_min',
        'potencia_max',
        'costo_por_kw',
        'costo_bateria_por_kw',
        'descripcion',
        'activo'
    ]
    
    list_editable = ['activo']
    
    def rango_potencia_display(self, obj):
        if obj.potencia_max:
            return f"{obj.potencia_min} - {obj.potencia_max} kW"
        else:
            return f"+{obj.potencia_min} kW"
    rango_potencia_display.short_description = 'Rango'
    
    def costo_por_kw_display(self, obj):
        return f"${obj.costo_por_kw:,.0f} USD/kW"
    costo_por_kw_display.short_description = 'Costo Instalación'
    
    def costo_bateria_por_kw_display(self, obj):
        return f"${obj.costo_bateria_por_kw:,.0f} USD/kW"
    costo_bateria_por_kw_display.short_description = 'Costo Batería'
    
    def activo_display(self, obj):
        return "✓" if obj.activo else "✗"
    activo_display.short_description = 'Activo'
    
    ordering = ['potencia_min']


@admin.register(FactorUbicacion)
class FactorUbicacionAdmin(admin.ModelAdmin):
    """Administrador para factores de ubicación"""
    
    list_display = [
        'provincia_display',
        'factor_irradiacion_display',
        'irradiacion_promedio_display',
        'activo'
    ]
    
    list_filter = ['activo']
    
    search_fields = ['provincia']
    
    fields = [
        'provincia',
        'factor_irradiacion',
        'irradiacion_promedio',
        'descripcion',
        'activo'
    ]
    
    list_editable = ['activo']
    
    def provincia_display(self, obj):
        return obj.get_provincia_display()
    provincia_display.short_description = 'Provincia'
    
    def factor_irradiacion_display(self, obj):
        color = "green" if obj.factor_irradiacion >= 1.0 else "orange" if obj.factor_irradiacion >= 0.9 else "red"
        return format_html(
            f'<span style="color: {color}; font-weight: bold;">{obj.factor_irradiacion:.2f}</span>'
        )
    factor_irradiacion_display.short_description = 'Factor'
    
    def irradiacion_promedio_display(self, obj):
        return f"{obj.irradiacion_promedio:.1f} kWh/m²/día"
    irradiacion_promedio_display.short_description = 'Irradiación'
    
    def activo_display(self, obj):
        return "✓" if obj.activo else "✗"
    activo_display.short_description = 'Activo'
    
    ordering = ['provincia']


@admin.register(FactorOrientacion)
class FactorOrientacionAdmin(admin.ModelAdmin):
    """Administrador para factores de orientación"""
    
    list_display = [
        'orientacion_display',
        'factor_eficiencia_display',
        'angulo_solar',
        'activo'
    ]
    
    list_filter = ['activo']
    
    fields = [
        'orientacion',
        'factor_eficiencia',
        'angulo_solar',
        'descripcion',
        'activo'
    ]
    
    list_editable = ['activo']
    
    def orientacion_display(self, obj):
        return f"{obj.get_orientacion_display()}"
    orientacion_display.short_description = 'Orientación'
    
    def factor_eficiencia_display(self, obj):
        percentage = obj.factor_eficiencia * 100
        color = "green" if percentage >= 90 else "orange" if percentage >= 70 else "red"
        return format_html(
            f'<span style="color: {color}; font-weight: bold;">{percentage:.0f}%</span>'
        )
    factor_eficiencia_display.short_description = 'Eficiencia'
    
    def activo_display(self, obj):
        return "✓" if obj.activo else "✗"
    activo_display.short_description = 'Activo'
    
    ordering = ['angulo_solar']


@admin.register(TipoTejado)
class TipoTejadoAdmin(admin.ModelAdmin):
    """Administrador para tipos de tejado"""
    
    list_display = [
        'tipo_display',
        'factor_complejidad_display',
        'angulo_optimo_display',
        'imagen_svg',
        'activo'
    ]
    
    list_filter = ['activo']
    
    fields = [
        'tipo',
        'factor_complejidad',
        'angulo_optimo',
        'imagen_svg',
        'descripcion',
        'activo'
    ]
    
    list_editable = ['activo']
    
    def tipo_display(self, obj):
        return obj.get_tipo_display()
    tipo_display.short_description = 'Tipo de Tejado'
    
    def factor_complejidad_display(self, obj):
        if obj.factor_complejidad == 1.0:
            return format_html('<span style="color: green;">1.0 (Normal)</span>')
        elif obj.factor_complejidad > 1.0:
            return format_html(
                f'<span style="color: orange;">{obj.factor_complejidad} (+{(obj.factor_complejidad-1)*100:.0f}%)</span>'
            )
        else:
            return format_html(
                f'<span style="color: blue;">{obj.factor_complejidad} ({(obj.factor_complejidad-1)*100:.0f}%)</span>'
            )
    factor_complejidad_display.short_description = 'Complejidad'
    
    def angulo_optimo_display(self, obj):
        return f"{obj.angulo_optimo}°"
    angulo_optimo_display.short_description = 'Ángulo Óptimo'
    
    def activo_display(self, obj):
        return "✓" if obj.activo else "✗"
    activo_display.short_description = 'Activo'


@admin.register(AnguloTejado)
class AnguloTejadoAdmin(admin.ModelAdmin):
    """Administrador para ángulos de tejado"""
    
    list_display = [
        'angulo_display',
        'factor_eficiencia_display',
        'descripcion',
        'recomendado',
        'imagen_svg',
        'activo'
    ]
    
    list_filter = ['activo', 'recomendado']
    
    fields = [
        'angulo',
        'factor_eficiencia',
        'descripcion',
        'recomendado',
        'imagen_svg',
        'activo'
    ]
    
    list_editable = ['activo', 'recomendado']
    
    def angulo_display(self, obj):
        star = " ⭐" if obj.recomendado else ""
        return f"{obj.angulo}°{star}"
    angulo_display.short_description = 'Ángulo'
    
    def factor_eficiencia_display(self, obj):
        calculated = obj.get_factor_inclinacion()
        percentage = calculated * 100
        color = "green" if percentage >= 90 else "orange" if percentage >= 80 else "red"
        return format_html(
            f'<span style="color: {color}; font-weight: bold;">{percentage:.0f}%</span>'
        )
    factor_eficiencia_display.short_description = 'Eficiencia'
    
    def recomendado_display(self, obj):
        return "⭐ SÍ" if obj.recomendado else ""
    recomendado_display.short_description = 'Recomendado'
    
    def activo_display(self, obj):
        return "✓" if obj.activo else "✗"
    activo_display.short_description = 'Activo'
    
    ordering = ['angulo']


# Personalización del sitio admin
admin.site.site_header = 'INGLAT - Administración'
admin.site.site_title = 'INGLAT Admin'
admin.site.index_title = 'Panel de Administración INGLAT'