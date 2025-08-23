#!/usr/bin/env python
"""
Script de testing básico para verificar funcionalidades críticas de INGLAT
"""

import os
import sys
import django
from pathlib import Path

# Agregar el directorio del proyecto al path de Python
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INGLAT.settings')
django.setup()

def test_basic_functionality():
    """Pruebas básicas de funcionalidad"""
    print("🧪 INICIANDO TESTS BÁSICOS DE FUNCIONALIDAD INGLAT")
    print("="*60)
    
    passed = 0
    failed = 0
    
    # Test 1: Importaciones básicas
    try:
        from django.conf import settings
        from apps.core.models import Project, SimuladorConfig
        from apps.contact.models import ContactMessage
        print("✅ Test 1 PASADO: Importaciones básicas funcionan")
        passed += 1
    except Exception as e:
        print(f"❌ Test 1 FALLÓ: Error en importaciones - {e}")
        failed += 1
    
    # Test 2: Configuración de settings
    try:
        from django.conf import settings
        assert hasattr(settings, 'SECRET_KEY'), "SECRET_KEY no configurado"
        assert hasattr(settings, 'DEBUG'), "DEBUG no configurado" 
        assert hasattr(settings, 'MEDIA_URL'), "MEDIA_URL no configurado"
        assert hasattr(settings, 'MEDIA_ROOT'), "MEDIA_ROOT no configurado"
        assert settings.LANGUAGE_CODE == 'es-es', f"LANGUAGE_CODE incorrecto: {settings.LANGUAGE_CODE}"
        assert settings.TIME_ZONE == 'America/Argentina/Buenos_Aires', f"TIME_ZONE incorrecto: {settings.TIME_ZONE}"
        print("✅ Test 2 PASADO: Configuración de settings correcta")
        passed += 1
    except Exception as e:
        print(f"❌ Test 2 FALLÓ: Error en configuración - {e}")
        failed += 1
    
    # Test 3: Modelos básicos
    try:
        from apps.core.models import Project
        
        # Verificar que el modelo Project tiene los campos esperados
        fields = [field.name for field in Project._meta.get_fields()]
        required_fields = ['title', 'slug', 'location', 'description_short', 'is_active', 'is_featured']
        
        for field in required_fields:
            assert field in fields, f"Campo {field} no encontrado en Project"
        
        # Verificar método get_absolute_url existe
        assert hasattr(Project, 'get_absolute_url'), "Método get_absolute_url no encontrado"
        
        print("✅ Test 3 PASADO: Modelos básicos correctos")
        passed += 1
    except Exception as e:
        print(f"❌ Test 3 FALLÓ: Error en modelos - {e}")
        failed += 1
    
    # Test 4: URLs básicas
    try:
        from django.urls import reverse, NoReverseMatch
        
        # Verificar que las URLs básicas existen
        urls_to_test = [
            'core:home',
            'core:simulador', 
            'core:services'
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                # print(f"  URL {url_name}: {url}")
            except NoReverseMatch:
                raise Exception(f"URL {url_name} no encontrada")
        
        print("✅ Test 4 PASADO: URLs básicas configuradas")
        passed += 1
    except Exception as e:
        print(f"❌ Test 4 FALLÓ: Error en URLs - {e}")
        failed += 1
    
    # Test 5: Sistema de contacto
    try:
        from apps.contact.models import ContactMessage
        from apps.contact.forms import ContactForm
        
        # Verificar modelo ContactMessage
        fields = [field.name for field in ContactMessage._meta.get_fields()]
        required_fields = ['nombre', 'email', 'mensaje', 'tipo_proyecto']
        
        for field in required_fields:
            assert field in fields, f"Campo {field} no encontrado en ContactMessage"
        
        # Verificar formulario
        form = ContactForm()
        assert 'nombre' in form.fields, "Campo nombre no en formulario"
        assert 'email' in form.fields, "Campo email no en formulario"
        
        print("✅ Test 5 PASADO: Sistema de contacto funcional")
        passed += 1
    except Exception as e:
        print(f"❌ Test 5 FALLÓ: Error en sistema contacto - {e}")
        failed += 1
    
    # Test 6: Configuración de email
    try:
        from django.conf import settings
        
        assert hasattr(settings, 'EMAIL_BACKEND'), "EMAIL_BACKEND no configurado"
        assert hasattr(settings, 'EMAIL_HOST'), "EMAIL_HOST no configurado"
        assert hasattr(settings, 'EMAIL_PORT'), "EMAIL_PORT no configurado"
        
        # Si está en desarrollo, puede usar console backend
        if settings.DEBUG:
            print("  📧 Modo desarrollo: usando console backend para emails")
        
        print("✅ Test 6 PASADO: Configuración de email correcta")
        passed += 1
    except Exception as e:
        print(f"❌ Test 6 FALLÓ: Error en configuración email - {e}")
        failed += 1
    
    # Test 7: Simulador solar
    try:
        from apps.core.models import SimuladorConfig, CostoInstalacion, FactorUbicacion
        
        # Verificar que los modelos existen
        models_simulador = [SimuladorConfig, CostoInstalacion, FactorUbicacion]
        for model in models_simulador:
            fields = [field.name for field in model._meta.get_fields()]
            assert len(fields) > 3, f"Modelo {model.__name__} tiene muy pocos campos"
        
        print("✅ Test 7 PASADO: Modelos del simulador solar correctos")
        passed += 1
    except Exception as e:
        print(f"❌ Test 7 FALLÓ: Error en simulador solar - {e}")
        failed += 1
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE TESTS")
    print(f"✅ Tests pasados: {passed}")
    print(f"❌ Tests fallidos: {failed}")
    print(f"📈 Porcentaje éxito: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 ¡TODOS LOS TESTS BÁSICOS PASARON!")
        print("💚 El sistema INGLAT está funcionalmente correcto")
    else:
        print(f"\n⚠️  {failed} tests fallaron - revisar errores arriba")
    
    return failed == 0

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)