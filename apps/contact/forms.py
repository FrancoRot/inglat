# -*- coding: utf-8 -*-
from django import forms
from .models import ContactMessage, TipoProyecto


class ContactForm(forms.ModelForm):
    """Formulario de contacto con validaciones personalizadas"""
    
    class Meta:
        model = ContactMessage
        fields = ['nombre', 'email', 'telefono', 'tipo_proyecto', 'mensaje']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tu nombre completo',
                'required': True,
                'maxlength': 100
            }),
            
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'tu@email.com',
                'required': True
            }),
            
            'telefono': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+54 XX XXXX XXXX (opcional)',
                'maxlength': 20
            }),
            
            'tipo_proyecto': forms.Select(attrs={
                'class': 'form-input form-select',
                'required': True
            }),
            
            'mensaje': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Contanos sobre tu proyecto: ubicación, consumo actual, tipo de instalación deseada, etc.',
                'rows': 5,
                'required': True,
                'maxlength': 1000
            })
        }
        
        labels = {
            'nombre': 'Nombre completo *',
            'email': 'Email *',
            'telefono': 'Teléfono',
            'tipo_proyecto': 'Tipo de proyecto *',
            'mensaje': 'Tu mensaje *'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar choices del tipo_proyecto con descripción
        self.fields['tipo_proyecto'].choices = [
            ('', 'Seleccioná el tipo de proyecto...'),
            (TipoProyecto.RESIDENCIAL, 'Instalación Residencial'),
            (TipoProyecto.COMERCIAL, 'Instalación Comercial'),
            (TipoProyecto.INDUSTRIAL, 'Instalación Industrial'),
            (TipoProyecto.AUTOCONSUMO, 'Sistema de Autoconsumo'),
            (TipoProyecto.BATERIAS, 'Sistema con Baterías'),
            (TipoProyecto.MANTENIMIENTO, 'Mantenimiento'),
            (TipoProyecto.CONSULTORIA, 'Consultoría Energética'),
            (TipoProyecto.OTRO, 'Otro')
        ]

    def clean_nombre(self):
        """Validación personalizada para el nombre"""
        nombre = self.cleaned_data.get('nombre', '').strip()
        
        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')
            
        if len(nombre) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
            
        # Verificar que no sea solo números o caracteres especiales
        if not any(c.isalpha() for c in nombre):
            raise forms.ValidationError('El nombre debe contener al menos una letra.')
            
        return nombre.title()

    def clean_email(self):
        """Validación personalizada para el email"""
        email = self.cleaned_data.get('email', '').strip().lower()
        
        if not email:
            raise forms.ValidationError('El email es obligatorio.')
            
        # Verificar dominios comunes mal escritos
        dominios_comunes = {
            'gmail.co': 'gmail.com',
            'hotmail.co': 'hotmail.com',
            'yahoo.co': 'yahoo.com',
            'outlook.co': 'outlook.com'
        }
        
        for incorrecto, correcto in dominios_comunes.items():
            if email.endswith(incorrecto):
                raise forms.ValidationError(
                    f'¿Quisiste escribir {correcto}? Por favor verificá tu email.'
                )
        
        return email

    def clean_telefono(self):
        """Validación personalizada para el teléfono (opcional)"""
        telefono = self.cleaned_data.get('telefono', '').strip()
        
        if telefono:
            # Limpiar caracteres no numéricos excepto + y espacios
            telefono_limpio = ''.join(c for c in telefono if c.isdigit() or c in '+- ()')
            
            # Verificar longitud mínima para números argentinos
            numeros_solo = ''.join(c for c in telefono_limpio if c.isdigit())
            if len(numeros_solo) < 9:
                raise forms.ValidationError('El teléfono debe tener al menos 9 dígitos.')
                
            if len(numeros_solo) > 15:
                raise forms.ValidationError('El teléfono no puede tener más de 15 dígitos.')
                
            return telefono_limpio
        
        return telefono

    def clean_mensaje(self):
        """Validación personalizada para el mensaje"""
        mensaje = self.cleaned_data.get('mensaje', '').strip()
        
        if not mensaje:
            raise forms.ValidationError('El mensaje es obligatorio.')
            
        if len(mensaje) < 10:
            raise forms.ValidationError('El mensaje debe tener al menos 10 caracteres.')
            
        if len(mensaje) > 1000:
            raise forms.ValidationError('El mensaje no puede exceder los 1000 caracteres.')
            
        # Verificar que no sea spam básico
        palabras_spam = ['click aquí', 'oferta especial', 'gratis', 'dinero fácil']
        mensaje_lower = mensaje.lower()
        
        for palabra_spam in palabras_spam:
            if palabra_spam in mensaje_lower:
                raise forms.ValidationError('Tu mensaje parece contener spam. Por favor, reescribelo.')
        
        return mensaje

    def clean(self):
        """Validación general del formulario"""
        cleaned_data = super().clean()
        
        # Verificar que al menos tenga teléfono o email válido
        email = cleaned_data.get('email')
        telefono = cleaned_data.get('telefono')
        
        if not email and not telefono:
            raise forms.ValidationError(
                'Debés proporcionar al menos un email o teléfono para poder contactarte.'
            )
        
        return cleaned_data