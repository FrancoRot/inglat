#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os
import sys

def create_puerto_penasco_solar_image():
    """
    Genera una imagen representativa del parque solar de Puerto Peñasco
    usando matplotlib para crear una visualización moderna y atractiva.
    """
    
    # Configurar el tamaño y DPI para alta calidad
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    
    # Colores para el tema solar
    desert_color = '#D4A574'
    sky_blue = '#87CEEB'
    solar_blue = '#1E3A8A'
    solar_gold = '#FFD700'
    panel_color = '#2D3748'
    
    # Fondo del cielo con gradiente
    sky_gradient = LinearSegmentedColormap.from_list('sky', [sky_blue, '#FFA500', '#FFE4B5'])
    ax.imshow([[0, 1]], extent=[0, 16, 6, 9], aspect='auto', cmap=sky_gradient, alpha=0.8)
    
    # Suelo del desierto
    desert = patches.Rectangle((0, 0), 16, 6, facecolor=desert_color, alpha=0.7)
    ax.add_patch(desert)
    
    # Sol
    sol = patches.Circle((13, 7.5), 0.8, facecolor=solar_gold, edgecolor='#FF8C00', linewidth=2)
    ax.add_patch(sol)
    
    # Rayos del sol
    for angle in np.linspace(0, 2*np.pi, 12):
        x_ray = 13 + 1.2 * np.cos(angle)
        y_ray = 7.5 + 1.2 * np.sin(angle)
        x_ray_end = 13 + 1.6 * np.cos(angle)
        y_ray_end = 7.5 + 1.6 * np.sin(angle)
        ax.plot([x_ray, x_ray_end], [y_ray, y_ray_end], color=solar_gold, linewidth=3, alpha=0.7)
    
    # Crear paneles solares en perspectiva
    panel_positions = [
        (2, 3, 0.3, 1.5), (4, 3, 0.3, 1.5), (6, 3, 0.3, 1.5),
        (8, 3, 0.3, 1.5), (10, 3, 0.3, 1.5), (12, 3, 0.3, 1.5),
        (2.5, 2, 0.3, 1.5), (4.5, 2, 0.3, 1.5), (6.5, 2, 0.3, 1.5),
        (8.5, 2, 0.3, 1.5), (10.5, 2, 0.3, 1.5), (12.5, 2, 0.3, 1.5),
        (3, 1, 0.25, 1.2), (5, 1, 0.25, 1.2), (7, 1, 0.25, 1.2),
        (9, 1, 0.25, 1.2), (11, 1, 0.25, 1.2),
    ]
    
    for x, y, width, height in panel_positions:
        # Panel principal
        panel = patches.Rectangle((x, y), height, width, 
                                facecolor=panel_color, 
                                edgecolor='#4A5568', 
                                linewidth=1,
                                alpha=0.9)
        ax.add_patch(panel)
        
        # Brillo en el panel para simular reflejo solar
        highlight = patches.Rectangle((x + 0.1, y + 0.05), height - 0.2, width - 0.1,
                                    facecolor=solar_blue, alpha=0.3)
        ax.add_patch(highlight)
        
        # Líneas de los paneles fotovoltaicos
        for i in range(3):
            line_x = x + (i + 1) * height / 4
            ax.plot([line_x, line_x], [y, y + width], color='#718096', linewidth=0.5, alpha=0.7)
    
    # Torres de transmisión eléctrica
    tower_positions = [(1, 4), (14, 4.5)]
    for tx, ty in tower_positions:
        # Estructura de la torre
        tower_lines = [
            [(tx, ty), (tx, ty + 2)],  # Vertical principal
            [(tx - 0.3, ty + 1.5), (tx + 0.3, ty + 1.5)],  # Horizontal
            [(tx - 0.2, ty + 1), (tx + 0.2, ty + 1)],  # Horizontal menor
        ]
        for line in tower_lines:
            ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 
                   color='#4A5568', linewidth=2)
    
    # Cables de transmisión
    x_cable = np.linspace(1.3, 13.7, 100)
    y_cable = 5.5 + 0.1 * np.sin(x_cable * 0.5)  # Catenaria simulada
    ax.plot(x_cable, y_cable, color='#2D3748', linewidth=1.5, alpha=0.8)
    
    # Texto principal
    ax.text(8, 8.5, 'PUERTO PEÑASCO', fontsize=24, fontweight='bold', 
            ha='center', color=solar_blue, family='sans-serif')
    ax.text(8, 8, 'PARQUE SOLAR 1,000 MW', fontsize=16, fontweight='bold', 
            ha='center', color=panel_color, family='sans-serif')
    ax.text(8, 7.6, 'El más grande de América Latina', fontsize=12, 
            ha='center', color='#666666', style='italic', family='sans-serif')
    
    # Estadísticas en el lado izquierdo
    stats_text = [
        "1,000 MW de potencia",
        "2,000 hectáreas",
        "1.6 millones de personas",
        "$1,600 millones USD"
    ]
    
    for i, stat in enumerate(stats_text):
        ax.text(0.5, 6.5 - i*0.4, f"• {stat}", fontsize=10, 
                color=solar_blue, fontweight='bold', family='sans-serif')
    
    # Logo de México (bandera estilizada)
    mexico_flag = patches.Rectangle((14.5, 0.3), 1.2, 0.8, facecolor='white', edgecolor='gray')
    ax.add_patch(mexico_flag)
    green_stripe = patches.Rectangle((14.5, 0.3), 0.4, 0.8, facecolor='#006847')
    red_stripe = patches.Rectangle((15.3, 0.3), 0.4, 0.8, facecolor='#CE1126')
    ax.add_patch(green_stripe)
    ax.add_patch(red_stripe)
    ax.text(15.1, 0.15, 'MÉXICO', fontsize=8, ha='center', fontweight='bold', color='#333333')
    
    # Configuración final
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Guardar la imagen
    output_path = '/mnt/c/Users/franc/Desktop/INGLAT/codigo/media/noticias/imagenes/puerto_penasco_solar_1000mw.jpg'
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none', format='jpg', quality=95)
    plt.close()
    
    print(f"Imagen generada exitosamente: {output_path}")
    return output_path

if __name__ == "__main__":
    image_path = create_puerto_penasco_solar_image()
    print(f"Imagen creada en: {image_path}")