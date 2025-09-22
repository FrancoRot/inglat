# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class TipoProyecto(models.TextChoices):
    """Tipos de proyecto para instalaciones solares"""
    RESIDENCIAL = 'residencial', 'Instalación Residencial'
    COMERCIAL = 'comercial', 'Instalación Comercial'  
    INDUSTRIAL = 'industrial', 'Instalación Industrial'
    AUTOCONSUMO = 'autoconsumo', 'Sistema de Autoconsumo'
    BATERIAS = 'baterias', 'Sistema con Baterías'
    MANTENIMIENTO = 'mantenimiento', 'Mantenimiento'
    CONSULTORIA = 'consultoria', 'Consultoría Energética'
    OTRO = 'otro', 'Otro'


class ContactMessage(models.Model):
    """Modelo para almacenar mensajes de contacto desde el formulario web"""
    
    # Información personal
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
        verbose_name="Teléfono",
        help_text="Opcional - formato: +54 XX XXXX XXXX"
    )
    
    # Información del proyecto
    tipo_proyecto = models.CharField(
        max_length=20,
        choices=TipoProyecto.choices,
        default=TipoProyecto.RESIDENCIAL,
        verbose_name="Tipo de proyecto"
    )
    
    mensaje = models.TextField(
        verbose_name="Mensaje",
        help_text="Contanos sobre tu proyecto o consulta"
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de creación"
    )
    
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name="Dirección IP"
    )
    
    # Control interno
    leido = models.BooleanField(
        default=False,
        verbose_name="Leído"
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
        """Marca el mensaje como leído"""
        self.leido = True
        self.save(update_fields=['leido'])

    def marcar_como_respondido(self):
        """Marca el mensaje como respondido"""
        self.respondido = True
        self.leido = True
        self.save(update_fields=['respondido', 'leido'])