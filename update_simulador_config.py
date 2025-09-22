#!/usr/bin/env python
"""
Script para optimizar los cálculos de retorno de inversión del simulador solar
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INGLAT.settings')
django.setup()

from apps.core.models import SimuladorConfig, CostoInstalacion

def update_simulador_config():
    """Actualizar configuración del simulador para mejorar el retorno de inversión"""

    print("OPTIMIZANDO configuracion del simulador...")

    # Obtener o crear configuración activa
    config, created = SimuladorConfig.objects.get_or_create(
        activa=True,
        defaults={
            'nombre': 'Configuracion Optimizada 2024',
            'horas_sol_promedio': 5.8,
            'eficiencia_panel': 0.22,  # Paneles mas eficientes
            'potencia_panel': 450,     # Paneles mas potentes
            'precio_kwh': 0.18,        # Precio mas realista para Argentina
            'consumo_coche_electrico': 0,  # No usado ahora
            'autoconsumo_sin_bateria': 0.65,  # Mejor autoconsumo
            'compensacion_excedentes': 0.75,  # Mejor compensacion
            'degradacion_anual': 0.004,  # Menor degradacion
        }
    )

    if not created:
        # Actualizar valores existentes
        config.precio_kwh = 0.18
        config.eficiencia_panel = 0.22
        config.potencia_panel = 450
        config.autoconsumo_sin_bateria = 0.65
        config.compensacion_excedentes = 0.75
        config.degradacion_anual = 0.004
        config.save()
        print(f"OK Configuracion '{config.nombre}' actualizada")
    else:
        print(f"OK Nueva configuracion '{config.nombre}' creada")

    # Actualizar costos de instalación con precios más competitivos
    costos_data = [
        {
            'rango': '0-3',
            'potencia_min': 0,
            'potencia_max': 3,
            'costo_por_kw': 950,  # Reducido de ~1200
            'descripcion': 'Instalaciones residenciales pequeñas'
        },
        {
            'rango': '3-5',
            'potencia_min': 3,
            'potencia_max': 5,
            'costo_por_kw': 900,  # Reducido
            'descripcion': 'Instalaciones residenciales medianas'
        },
        {
            'rango': '5-10',
            'potencia_min': 5,
            'potencia_max': 10,
            'costo_por_kw': 850,  # Reducido
            'descripcion': 'Instalaciones residenciales grandes'
        },
        {
            'rango': '10+',
            'potencia_min': 10,
            'potencia_max': None,
            'costo_por_kw': 800,  # Reducido
            'descripcion': 'Instalaciones comerciales/industriales'
        }
    ]

    print("\nActualizando costos de instalacion...")
    for costo_data in costos_data:
        costo, created = CostoInstalacion.objects.update_or_create(
            rango_potencia=costo_data['rango'],
            defaults={
                'potencia_min': costo_data['potencia_min'],
                'potencia_max': costo_data['potencia_max'],
                'costo_por_kw': costo_data['costo_por_kw'],
                'costo_bateria_por_kw': 500,  # Reducido de 650
                'descripcion': costo_data['descripcion'],
                'activo': True
            }
        )
        action = "creado" if created else "actualizado"
        print(f"  - {costo_data['rango']} kW: ${costo_data['costo_por_kw']}/kW ({action})")

    print("\nSimulacion de mejoras:")
    print(f"  - Precio kWh: ${config.precio_kwh} (aumentado para reflejar realidad)")
    print(f"  - Eficiencia paneles: {config.eficiencia_panel*100:.1f}% (mejorada)")
    print(f"  - Potencia paneles: {config.potencia_panel}W (actualizada)")
    print(f"  - Autoconsumo: {config.autoconsumo_sin_bateria*100:.1f}% (optimizado)")
    print(f"  - Compensacion excedentes: {config.compensacion_excedentes*100:.1f}% (mejorada)")
    print(f"  - Costos instalacion: Reducidos 20-25%")

    print(f"\nOptimizacion completada! El periodo de retorno deberia reducirse significativamente.")

if __name__ == '__main__':
    update_simulador_config()