from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .forms import ContactForm
from .models import ContactMessage


@method_decorator(csrf_protect, name='dispatch')
class ContactView(TemplateView):
    """Vista principal de contacto con formulario integrado"""
    template_name = 'contact/contact.html'
    
    def get_context_data(self, **kwargs):
        """Agregar formulario y datos adicionales al contexto"""
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        context['page_title'] = 'Contacto'
        context['page_description'] = 'Contacta con INGLAT para tu proyecto solar. Te ayudamos a encontrar la mejor solucion energetica.'
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
            
            # Mensaje de exito
            messages.success(
                request, 
                f'Gracias {contact_message.nombre}! Tu mensaje ha sido enviado correctamente. '
                'Nos pondremos en contacto contigo en las proximas 24 horas.'
            )
            
            # Verificar si es una peticion AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Mensaje enviado correctamente',
                    'redirect_url': '/contacto/?success=1'
                })
            
            # Redireccionar despues del POST exitoso
            return redirect('contact:contact_success')
        
        else:
            # Formulario con errores
            messages.error(
                request,
                'Por favor revisa los errores en el formulario y vuelve a intentar.'
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


def contact_success(request):
    """Vista de exito despues del envio del formulario"""
    context = {
        'page_title': 'Mensaje Enviado',
        'page_description': 'Tu mensaje ha sido enviado correctamente.'
    }
    return render(request, 'contact/contact_success.html', context)


# Vista de funcion como alternativa (mantener compatibilidad)
def contact(request):
    """Vista de funcion para contacto - redirige a la clase"""
    view = ContactView.as_view()
    return view(request)