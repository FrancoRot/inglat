# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from .forms import ContactForm
from .models import ContactMessage
import logging
import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


@method_decorator(csrf_protect, name='dispatch')
class ContactView(TemplateView):
    """Vista principal de contacto con formulario integrado"""
    template_name = 'contact/contact.html'
    
    def get_context_data(self, **kwargs):
        """Agregar formulario y datos adicionales al contexto"""
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        context['page_title'] = 'Contacto'
        context['page_description'] = 'Contactá con INGLAT para tu proyecto solar. Te ayudamos a encontrar la mejor solución energética.'
        return context
    
    def post(self, request, *args, **kwargs):
        """Procesar el formulario de contacto"""
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Crear el mensaje de contacto
            contact_message = form.save(commit=False)
            
            # Obtener la IP del usuario
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            contact_message.ip_address = ip
            
            # Guardar el mensaje
            contact_message.save()
            
            # Verificar configuración de email antes de enviar
            email_config_ok = self._verificar_configuracion_email()
            
            if not email_config_ok:
                # Si la configuración de email no está correcta, solo guardar el mensaje
                messages.warning(
                    request, 
                    f'Gracias {contact_message.nombre}! Tu mensaje ha sido guardado correctamente. '
                    'Nos pondremos en contacto contigo pronto. (Nota: El envío automático de emails está temporalmente deshabilitado)'
                )
            else:
                # Enviar emails si la configuración está correcta
                email_errors = []
                
                # Enviar email de notificación a la empresa
                if not self._enviar_email_notificacion(contact_message, request):
                    email_errors.append("Error al enviar notificación a la empresa")
                
                # Enviar email de confirmación al cliente
                if not self._enviar_email_confirmacion_cliente(contact_message, request):
                    email_errors.append("Error al enviar confirmación al cliente")
                
                if email_errors:
                    # Si hay errores de email, mostrar mensaje específico
                    messages.warning(
                        request, 
                        f'Gracias {contact_message.nombre}! Tu mensaje ha sido guardado correctamente. '
                        f'Hubo problemas con el envío automático de emails: {", ".join(email_errors)}. '
                        'Nos pondremos en contacto contigo pronto.'
                    )
                else:
                    # Éxito completo
                    messages.success(
                        request, 
                        f'Gracias {contact_message.nombre}! Tu mensaje ha sido enviado correctamente. '
                        'Nos pondremos en contacto contigo en las próximas 24 horas.'
                    )
            
            # Verificar si es una petición AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Mensaje enviado correctamente',
                    'redirect_url': '/contacto/?success=1'
                })
            
            # Redireccionar después del POST exitoso
            return redirect('contact:contact_success')
        
        else:
            # Formulario con errores
            messages.error(
                request,
                'Por favor revisá los errores en el formulario y volvé a intentar.'
            )
            
            # Si es AJAX, devolver errores
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                    'message': 'Hay errores en el formulario'
                })
        
        # Renderizar con errores
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
    
    def _verificar_configuracion_email(self):
        """Verificar que la configuración de email esté correcta"""
        try:
            # Verificar que las variables necesarias estén configuradas
            required_settings = [
                'EMAIL_HOST',
                'EMAIL_PORT', 
                'EMAIL_HOST_USER',
                'EMAIL_HOST_PASSWORD',
                'DEFAULT_FROM_EMAIL'
            ]
            
            for setting in required_settings:
                value = getattr(settings, setting, None)
                if not value:
                    logger.error(f'Configuración de email faltante: {setting}')
                    return False
            
            # Verificar que la contraseña no esté vacía
            if not settings.EMAIL_HOST_PASSWORD:
                logger.error('EMAIL_HOST_PASSWORD está vacío')
                return False
                
            return True
            
        except Exception as e:
            logger.error(f'Error verificando configuración de email: {e}')
            return False
    
    def _enviar_email_notificacion(self, contact_message, request):
        """Enviar email de notificación cuando se recibe un mensaje de contacto"""
        try:
            # Preparar contexto para el email
            context = {
                'mensaje': contact_message,
                'site_url': request.build_absolute_uri('/'),
                'admin_url': request.build_absolute_uri('/admin/contact/contactmessage/')
            }
            
            # Asunto del email
            asunto = f'Nuevo mensaje de contacto - {contact_message.get_tipo_proyecto_display()}'
            
            # Contenido del email en texto plano
            mensaje_texto = f"""
Nuevo mensaje de contacto recibido en INGLAT

Nombre: {contact_message.nombre}
Email: {contact_message.email}
Teléfono: {contact_message.telefono or 'No proporcionado'}
Tipo de Proyecto: {contact_message.get_tipo_proyecto_display()}

Mensaje:
{contact_message.mensaje}

Fecha: {contact_message.fecha_creacion.strftime('%d/%m/%Y %H:%M')}
IP: {contact_message.ip_address or 'No disponible'}

Para responder, visitá: {context['admin_url']}{contact_message.id}/

---
INGLAT - Sistema de Notificaciones
"""
            
            # Crear mensaje con headers adicionales para mejorar la entrega
            from django.core.mail import EmailMessage
            
            email = EmailMessage(
                subject=asunto,
                body=mensaje_texto,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['info@inglat.com', 'contacto@inglat.com'],  # Enviar a ambas cuentas
                headers={
                    'X-Priority': '1',  # Alta prioridad
                    'X-MSMail-Priority': 'High',
                    'Importance': 'high',
                    'X-Mailer': 'INGLAT Contact System',
                    'Reply-To': contact_message.email,  # Para responder directamente al cliente
                }
            )
            
            # Enviar email
            email.send()
            
            logger.info(f'Email de notificación enviado para mensaje de {contact_message.nombre}')
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f'Error de autenticación SMTP: {e}')
            return False
        except smtplib.SMTPException as e:
            logger.error(f'Error SMTP: {e}')
            return False
        except Exception as e:
            logger.error(f'Error enviando email de notificación: {e}')
            return False
    
    def _enviar_email_confirmacion_cliente(self, contact_message, request):
        """Enviar email de confirmación al cliente"""
        try:
            # Preparar contexto para el email del cliente
            context = {
                'contact_message': contact_message,
                'site_url': request.build_absolute_uri('/'),
                'email_subject': 'Hemos recibido tu mensaje en INGLAT'
            }
            
            # Renderizar template HTML
            html_content = render_to_string('emails/customer_confirmation.html', context)
            text_content = strip_tags(html_content)
            
            # Asunto del email
            asunto = f"Hemos recibido tu mensaje en INGLAT ☀️"
            
            # Crear mensaje multipart (HTML + texto plano)
            msg = EmailMultiAlternatives(
                subject=asunto,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[contact_message.email],
            )
            msg.attach_alternative(html_content, "text/html")
            
            # Enviar email
            msg.send()
            
            logger.info(f'Email de confirmación enviado a {contact_message.email}')
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f'Error de autenticación SMTP al cliente: {e}')
            return False
        except smtplib.SMTPException as e:
            logger.error(f'Error SMTP al cliente: {e}')
            return False
        except Exception as e:
            logger.error(f'Error enviando email de confirmación al cliente: {e}')
            return False


def contact_success(request):
    """Vista de éxito después del envío del formulario"""
    context = {
        'page_title': 'Mensaje Enviado',
        'page_description': 'Tu mensaje ha sido enviado correctamente.'
    }
    return render(request, 'contact/contact_success.html', context)


# Vista de funcion como alternativa (mantener compatibilidad)
def contact(request):
    """Vista de función para contacto - redirige a la clase"""
    view = ContactView.as_view()
    return view(request)