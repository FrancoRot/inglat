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
from .forms import ContactForm
from .models import ContactMessage
import logging

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
            
            # Enviar email de notificación
            self._enviar_email_notificacion(contact_message, request)
            
            # Mensaje de éxito
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
            
            # Enviar email
            send_mail(
                subject=asunto,
                message=mensaje_texto,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@inglat.com'),
                recipient_list=['contacto@inglat.com'],
                fail_silently=False,
            )
            
            logger.info(f'Email de notificación enviado para mensaje de {contact_message.nombre}')
            
        except Exception as e:
            logger.error(f'Error enviando email de notificación: {e}')
            # No interrumpir el flujo si falla el email


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