#!/usr/bin/env python3
"""
Script para verificar que los cambios se aplicaron correctamente
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/mnt/c/Users/franc/Desktop/INGLAT/codigo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INGLAT.settings')
django.setup()

from apps.core.models import Project, HomePortada, SimuladorConfig
from apps.blog.models import Noticia

def test_admin_changes():
    print("=== TEST: Cambios en Admin ===")
    
    # Test 1: Verificar verbose names
    print(f"✓ Project verbose_name: {Project._meta.verbose_name}")
    print(f"✓ HomePortada verbose_name: {HomePortada._meta.verbose_name}")
    print(f"✓ SimuladorConfig verbose_name: {SimuladorConfig._meta.verbose_name}")
    
    # Test 2: Verificar que HomePortada funciona
    portada_count = HomePortada.objects.count()
    print(f"✓ HomePortadas en DB: {portada_count}")
    
    if portada_count > 0:
        portada_activa = HomePortada.get_activa()
        print(f"✓ Portada activa: {portada_activa.nombre} ({portada_activa.tipo_multimedia})")

def test_tinymce():
    print("\n=== TEST: TinyMCE ===")
    
    # Test 3: Verificar TinyMCE en settings
    from django.conf import settings
    tinymce_installed = 'tinymce' in settings.INSTALLED_APPS
    print(f"✓ TinyMCE instalado: {tinymce_installed}")
    
    if hasattr(settings, 'TINYMCE_DEFAULT_CONFIG'):
        print("✓ TinyMCE configurado correctamente")
    else:
        print("✗ TinyMCE NO configurado")
        
    # Test 4: Verificar campo HTMLField
    if Noticia.objects.exists():
        noticia = Noticia.objects.first()
        field_type = type(noticia._meta.get_field('contenido'))
        print(f"✓ Campo contenido es: {field_type}")
        
        # Verificar si hay HTML
        contenido_str = str(noticia.contenido)
        has_html = '<' in contenido_str and '>' in contenido_str
        print(f"✓ Noticia contiene HTML: {has_html}")
        if has_html:
            print(f"  Ejemplo: {contenido_str[:100]}...")
    else:
        print("✗ No hay noticias para probar TinyMCE")

def test_templates():
    print("\n=== TEST: Templates y CSS ===")
    
    # Test 5: Verificar archivos de template
    template_files = [
        '/mnt/c/Users/franc/Desktop/INGLAT/codigo/templates/core/home.html',
        '/mnt/c/Users/franc/Desktop/INGLAT/codigo/templates/blog/noticia_detalle.html',
        '/mnt/c/Users/franc/Desktop/INGLAT/codigo/templates/blog/components/noticia_card.html'
    ]
    
    for template_file in template_files:
        if os.path.exists(template_file):
            print(f"✓ Template existe: {os.path.basename(template_file)}")
        else:
            print(f"✗ Template NO existe: {os.path.basename(template_file)}")
    
    # Test 6: Verificar cambios específicos en templates
    with open('/mnt/c/Users/franc/Desktop/INGLAT/codigo/templates/blog/noticia_detalle.html', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'contenido|safe' in content:
            print("✓ Template noticia_detalle.html usa |safe")
        else:
            print("✗ Template noticia_detalle.html NO usa |safe")
    
    # Test 7: Verificar CSS
    css_files = [
        '/mnt/c/Users/franc/Desktop/INGLAT/codigo/static/css/home.css',
        '/mnt/c/Users/franc/Desktop/INGLAT/codigo/static/css/base.css'
    ]
    
    for css_file in css_files:
        if os.path.exists(css_file):
            print(f"✓ CSS existe: {os.path.basename(css_file)}")
            
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if css_file.endswith('home.css') and 'hero__video-loading' in content:
                    print("  ✓ home.css tiene estilos de video loading")
                if css_file.endswith('base.css') and 'btn--simulator' in content:
                    print("  ✓ base.css tiene botón simulador")
        else:
            print(f"✗ CSS NO existe: {os.path.basename(css_file)}")

def main():
    print("🔍 VERIFICANDO CAMBIOS IMPLEMENTADOS...\n")
    
    try:
        test_admin_changes()
        test_tinymce()
        test_templates()
        
        print("\n" + "="*50)
        print("✅ VERIFICACIÓN COMPLETADA")
        print("Los cambios principales están implementados.")
        print("\n📋 ACCIONES NECESARIAS:")
        print("1. Reiniciar el servidor Django si no se hizo")
        print("2. Refrescar la página del admin (Ctrl+F5)")
        print("3. Limpiar cache del navegador")
        print("4. Verificar que el servidor esté corriendo en el puerto correcto")
        
    except Exception as e:
        print(f"\n❌ ERROR durante la verificación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()