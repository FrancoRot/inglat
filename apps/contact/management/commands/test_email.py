# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import smtplib
import ssl


class Command(BaseCommand):
    help = 'Probar la configuración de email de Django'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            default='test@example.com',
            help='Email de destino para la prueba'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Iniciando prueba de configuración de email...'))
        
        # Verificar configuración
        self._verificar_configuracion()
        
        # Probar conexión SMTP
        self._probar_conexion_smtp()
        
        # Probar envío de email
        self._probar_envio_email(options['to'])

    def _verificar_configuracion(self):
        """Verificar que todas las configuraciones necesarias estén presentes"""
        self.stdout.write('\n📋 Verificando configuración...')
        
        configuraciones = {
            'EMAIL_HOST': settings.EMAIL_HOST,
            'EMAIL_PORT': settings.EMAIL_PORT,
            'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
            'EMAIL_HOST_PASSWORD': '***' if settings.EMAIL_HOST_PASSWORD else 'NO CONFIGURADO',
            'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
            'EMAIL_USE_SSL': settings.EMAIL_USE_SSL,
            'EMAIL_USE_TLS': settings.EMAIL_USE_TLS,
        }
        
        for key, value in configuraciones.items():
            if value:
                self.stdout.write(f'✅ {key}: {value}')
            else:
                self.stdout.write(self.style.ERROR(f'❌ {key}: NO CONFIGURADO'))
        
        # Verificar si la contraseña está configurada
        if not settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(self.style.WARNING(
                '\n⚠️  ADVERTENCIA: EMAIL_HOST_PASSWORD no está configurado. '
                'Necesitas configurar esta variable de entorno.'
            ))

    def _probar_conexion_smtp(self):
        """Probar la conexión SMTP directamente"""
        self.stdout.write('\n🔌 Probando conexión SMTP...')
        
        try:
            # Crear contexto SSL si es necesario
            if settings.EMAIL_USE_SSL:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(
                    settings.EMAIL_HOST, 
                    settings.EMAIL_PORT, 
                    timeout=30,
                    context=context
                )
            else:
                server = smtplib.SMTP(
                    settings.EMAIL_HOST, 
                    settings.EMAIL_PORT, 
                    timeout=30
                )
                if settings.EMAIL_USE_TLS:
                    server.starttls()
            
            # Intentar login
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            
            self.stdout.write(self.style.SUCCESS('✅ Conexión SMTP exitosa'))
            self.stdout.write(f'   Servidor: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
            self.stdout.write(f'   Usuario: {settings.EMAIL_HOST_USER}')
            
            # Cerrar conexión
            server.quit()
            
        except smtplib.SMTPAuthenticationError as e:
            self.stdout.write(self.style.ERROR(f'❌ Error de autenticación SMTP: {e}'))
            self.stdout.write(self.style.WARNING(
                '💡 Verifica que el usuario y contraseña sean correctos'
            ))
        except smtplib.SMTPConnectError as e:
            self.stdout.write(self.style.ERROR(f'❌ Error de conexión SMTP: {e}'))
            self.stdout.write(self.style.WARNING(
                '💡 Verifica que el host y puerto sean correctos'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error inesperado: {e}'))

    def _probar_envio_email(self, to_email):
        """Probar el envío de un email de prueba"""
        self.stdout.write(f'\n📧 Probando envío de email a {to_email}...')
        
        try:
            # Enviar email de prueba
            send_mail(
                subject='Prueba de configuración - INGLAT',
                message=f"""
Este es un email de prueba para verificar la configuración de email de INGLAT.

Configuración actual:
- Host: {settings.EMAIL_HOST}
- Puerto: {settings.EMAIL_PORT}
- SSL: {settings.EMAIL_USE_SSL}
- TLS: {settings.EMAIL_USE_TLS}
- Usuario: {settings.EMAIL_HOST_USER}

Si recibes este email, la configuración está funcionando correctamente.

---
INGLAT - Sistema de Email
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Email de prueba enviado correctamente'))
            self.stdout.write(f'   De: {settings.DEFAULT_FROM_EMAIL}')
            self.stdout.write(f'   Para: {to_email}')
            
        except smtplib.SMTPAuthenticationError as e:
            self.stdout.write(self.style.ERROR(f'❌ Error de autenticación: {e}'))
        except smtplib.SMTPException as e:
            self.stdout.write(self.style.ERROR(f'❌ Error SMTP: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error inesperado: {e}'))
        
        self.stdout.write('\n🎯 Prueba completada.')