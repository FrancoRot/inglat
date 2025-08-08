# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test email functionality for INGLAT contact system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test to',
            default='test@example.com'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['simple', 'html'],
            help='Type of test email',
            default='html'
        )

    def handle(self, *args, **options):
        email_to = options['email']
        email_type = options['type']
        
        self.stdout.write(
            self.style.SUCCESS(f'Testing INGLAT email system...')
        )
        
        # Mostrar configuración actual
        self.stdout.write(f'Email Host: {settings.EMAIL_HOST}')
        self.stdout.write(f'Email Port: {settings.EMAIL_PORT}')
        self.stdout.write(f'Email Use SSL: {settings.EMAIL_USE_SSL}')
        self.stdout.write(f'From Email: {settings.DEFAULT_FROM_EMAIL}')
        
        try:
            if email_type == 'simple':
                self._send_simple_test(email_to)
            else:
                self._send_html_test(email_to)
                
            self.stdout.write(
                self.style.SUCCESS(f'✅ Test email sent successfully to {email_to}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error sending test email: {e}')
            )
            logger.error(f'Email test failed: {e}')

    def _send_simple_test(self, email_to):
        """Send simple text email"""
        from django.core.mail import send_mail
        
        send_mail(
            subject='Test Email - INGLAT System',
            message='This is a test email from INGLAT contact system. If you receive this, email configuration is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_to],
            fail_silently=False,
        )

    def _send_html_test(self, email_to):
        """Send HTML email using templates"""
        
        # Mock contact message data for testing
        mock_contact = type('MockContact', (), {
            'id': 999,
            'nombre': 'Test User',
            'email': email_to,
            'telefono': '+54 11 1234-5678',
            'get_tipo_proyecto_display': lambda: 'Instalación Residencial',
            'fecha_creacion': type('MockDate', (), {
                'strftime': lambda fmt: '08/08/2024 15:30'
            })()
        })()
        
        # Prepare context
        context = {
            'contact_message': mock_contact,
            'site_url': 'https://www.inglat.com/',
            'email_subject': 'Test Email - INGLAT System'
        }
        
        # Render HTML content
        html_content = render_to_string('emails/customer_confirmation.html', context)
        text_content = strip_tags(html_content)
        
        # Create multipart message
        msg = EmailMultiAlternatives(
            subject='Test Email - INGLAT System ☀️',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_to],
        )
        msg.attach_alternative(html_content, "text/html")
        
        # Send email
        msg.send()