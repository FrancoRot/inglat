# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Project(models.Model):
    """Modelo para gestionar proyectos de INGLAT desde el panel de administracion"""
    
    title = models.CharField(
        max_length=200,
        verbose_name="Titulo del Proyecto",
        help_text="Nombre descriptivo del proyecto de instalacion solar"
    )
    
    location = models.CharField(
        max_length=200,
        verbose_name="Ubicacion",
        help_text="Provincia, Pais donde se realizo el proyecto"
    )
    
    date_completed = models.DateField(
        verbose_name="Fecha de Finalizacion",
        help_text="Fecha en que se completo el proyecto"
    )
    
    description_short = models.CharField(
        max_length=300,
        verbose_name="Descripcion Corta",
        help_text="Resumen breve del proyecto (maximo 300 caracteres)"
    )
    
    description_full = models.TextField(
        verbose_name="Descripcion Completa",
        help_text="Descripcion detallada del proyecto, tecnologia utilizada, beneficios obtenidos"
    )
    
    featured_image = models.ImageField(
        upload_to='projects/images/',
        verbose_name="Imagen Principal",
        help_text="Imagen representativa del proyecto (recomendado: 1200x800px)"
    )
    
    power_capacity = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Potencia Instalada",
        help_text="Ej: 50kW, 100kW, 2.5MW"
    )
    
    client_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Tipo de Cliente",
        help_text="Ej: Residencial, Comercial, Industrial"
    )
    
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Proyecto Destacado",
        help_text="Marcar para mostrar en la pagina principal"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Desmarcar para ocultar el proyecto del sitio web"
    )
    
    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        verbose_name="URL Slug",
        help_text="Se genera automaticamente desde el titulo"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creado el"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Actualizado el"
    )
    
    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-date_completed', '-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.location}"
    
    def save(self, *args, **kwargs):
        """Generar slug automaticamente desde el titulo"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """URL del proyecto individual (para futuras implementaciones)"""
        return reverse('core:project_detail', kwargs={'slug': self.slug})