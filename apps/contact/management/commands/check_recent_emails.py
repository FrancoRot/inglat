from django.core.management.base import BaseCommand
from apps.contact.models import ContactMessage
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Verificar emails enviados recientemente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Número de horas hacia atrás para buscar (default: 24)'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        cutoff_time = timezone.now() - timedelta(hours=hours)
        
        self.stdout.write(f'🔍 Buscando mensajes de contacto de las últimas {hours} horas...')
        
        # Buscar mensajes recientes
        recent_messages = ContactMessage.objects.filter(
            fecha_creacion__gte=cutoff_time
        ).order_by('-fecha_creacion')
        
        if not recent_messages.exists():
            self.stdout.write(self.style.WARNING(f'❌ No se encontraron mensajes en las últimas {hours} horas'))
            return
        
        self.stdout.write(f'📧 Se encontraron {recent_messages.count()} mensajes:')
        self.stdout.write('')
        
        for message in recent_messages:
            self.stdout.write(f'📋 Mensaje #{message.id}:')
            self.stdout.write(f'   Nombre: {message.nombre}')
            self.stdout.write(f'   Email: {message.email}')
            self.stdout.write(f'   Teléfono: {message.telefono or "No proporcionado"}')
            self.stdout.write(f'   Tipo: {message.get_tipo_proyecto_display()}')
            self.stdout.write(f'   Fecha: {message.fecha_creacion.strftime("%d/%m/%Y %H:%M:%S")}')
            self.stdout.write(f'   IP: {message.ip_address or "No disponible"}')
            self.stdout.write(f'   Leído: {"Sí" if message.leido else "No"}')
            self.stdout.write(f'   Respondido: {"Sí" if message.respondido else "No"}')
            self.stdout.write(f'   Mensaje: {message.mensaje[:100]}{"..." if len(message.mensaje) > 100 else ""}')
            self.stdout.write('')
        
        # Estadísticas
        total_messages = recent_messages.count()
        unread_messages = recent_messages.filter(leido=False).count()
        unresponded_messages = recent_messages.filter(respondido=False).count()
        
        self.stdout.write('📊 Estadísticas:')
        self.stdout.write(f'   Total de mensajes: {total_messages}')
        self.stdout.write(f'   No leídos: {unread_messages}')
        self.stdout.write(f'   No respondidos: {unresponded_messages}')
        
        if unread_messages > 0:
            self.stdout.write(self.style.WARNING(f'⚠️  Tienes {unread_messages} mensajes sin leer'))
        
        if unresponded_messages > 0:
            self.stdout.write(self.style.WARNING(f'⚠️  Tienes {unresponded_messages} mensajes sin responder'))

