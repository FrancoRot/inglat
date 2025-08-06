from django.db import models
from django.utils import timezone


class TipoProyecto(models.TextChoices):
    """Tipos de proyecto para instalaciones solares"""
    RESIDENCIAL = 'residencial', 'Instalacion Residencial'
    COMERCIAL = 'comercial', 'Instalacion Comercial'  
    INDUSTRIAL = 'industrial', 'Instalacion Industrial'
    AUTOCONSUMO = 'autoconsumo', 'Sistema de Autoconsumo'
    BATERIAS = 'baterias', 'Sistema con Baterias'
    MANTENIMIENTO = 'mantenimiento', 'Mantenimiento'
    CONSULTORIA = 'consultoria', 'Consultoria Energetica'
    OTRO = 'otro', 'Otro'


class ContactMessage(models.Model):
    """Modelo para almacenar mensajes de contacto desde el formulario web"""
    
    # Informacion personal
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre completo"
    )
    
    email = models.EmailField(
        verbose_name="Email"
    )
    
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefono",
        help_text="Opcional - formato: +54 XX XXXX XXXX"
    )
    
    # Informacion del proyecto
    tipo_proyecto = models.CharField(
        max_length=20,
        choices=TipoProyecto.choices,
        default=TipoProyecto.RESIDENCIAL,
        verbose_name="Tipo de proyecto"
    )
    
    mensaje = models.TextField(
        verbose_name="Mensaje",
        help_text="Cuentanos sobre tu proyecto o consulta"
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de creacion"
    )
    
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name="Direccion IP"
    )
    
    # Control interno
    leido = models.BooleanField(
        default=False,
        verbose_name="Leido"
    )
    
    respondido = models.BooleanField(
        default=False,
        verbose_name="Respondido"
    )
    
    notas_internas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas internas",
        help_text="Notas para uso interno del equipo"
    )

    class Meta:
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_proyecto_display()} ({self.fecha_creacion.strftime('%d/%m/%Y')})"

    def marcar_como_leido(self):
        """Marca el mensaje como leido"""
        self.leido = True
        self.save(update_fields=['leido'])

    def marcar_como_respondido(self):
        """Marca el mensaje como respondido"""
        self.respondido = True
        self.leido = True
        self.save(update_fields=['respondido', 'leido'])