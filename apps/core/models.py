# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError


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


# ===========================
# MODELOS PARA SIMULADOR SOLAR
# ===========================

class SimuladorConfig(models.Model):
    """Configuración global del simulador solar"""
    
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de Configuración",
        help_text="Nombre descriptivo para identificar esta configuración"
    )
    
    # Parámetros técnicos base
    horas_sol_promedio = models.FloatField(
        default=5.8,
        verbose_name="Horas de Sol Promedio (por día)",
        help_text="Promedio de horas de sol pico diarias en Argentina"
    )
    
    eficiencia_panel = models.FloatField(
        default=0.20,
        verbose_name="Eficiencia de Paneles (%)",
        help_text="Eficiencia promedio de paneles solares (0.20 = 20%)"
    )
    
    potencia_panel = models.IntegerField(
        default=400,
        verbose_name="Potencia por Panel (W)",
        help_text="Potencia en vatios de cada panel solar estándar"
    )
    
    # Precios
    precio_kwh = models.FloatField(
        default=0.12,
        verbose_name="Precio kWh (USD)",
        help_text="Precio promedio del kWh en Argentina (USD)"
    )
    
    consumo_coche_electrico = models.IntegerField(
        default=2500,
        verbose_name="Consumo Coche Eléctrico (kWh/año)",
        help_text="Consumo adicional anual estimado para coche eléctrico"
    )
    
    # Factores de autoconsumo
    autoconsumo_con_bateria = models.FloatField(
        default=0.80,
        verbose_name="Autoconsumo con Batería (%)",
        help_text="Porcentaje de autoconsumo con sistema de baterías (0.80 = 80%)"
    )
    
    autoconsumo_sin_bateria = models.FloatField(
        default=0.60,
        verbose_name="Autoconsumo sin Batería (%)",
        help_text="Porcentaje de autoconsumo sin sistema de baterías (0.60 = 60%)"
    )
    
    compensacion_excedentes = models.FloatField(
        default=0.5,
        verbose_name="Factor Compensación Excedentes",
        help_text="Factor de compensación por excedentes (0.5 = 50% del precio kWh)"
    )
    
    degradacion_anual = models.FloatField(
        default=0.005,
        verbose_name="Degradación Anual Paneles",
        help_text="Degradación anual de paneles solares (0.005 = 0.5%)"
    )
    
    # Control
    activa = models.BooleanField(
        default=True,
        verbose_name="Configuración Activa",
        help_text="Solo una configuración puede estar activa a la vez"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )
    
    class Meta:
        verbose_name = "Configuración del Simulador"
        verbose_name_plural = "Configuraciones del Simulador"
        ordering = ['-activa', '-fecha_actualizacion']
    
    def __str__(self):
        estado = "ACTIVA" if self.activa else "Inactiva"
        return f"{self.nombre} ({estado})"
    
    def clean(self):
        """Validar que solo hay una configuración activa"""
        if self.activa:
            otras_activas = SimuladorConfig.objects.filter(activa=True)
            if self.pk:
                otras_activas = otras_activas.exclude(pk=self.pk)
            if otras_activas.exists():
                raise ValidationError("Solo puede haber una configuración activa a la vez")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @classmethod
    def get_activa(cls):
        """Obtener la configuración activa actual"""
        try:
            return cls.objects.get(activa=True)
        except cls.DoesNotExist:
            # Crear configuración por defecto si no existe ninguna
            return cls.objects.create(
                nombre="Configuración por Defecto",
                activa=True
            )


class CostoInstalacion(models.Model):
    """Costos de instalación por rangos de potencia"""
    
    RANGOS_POTENCIA = [
        ('0-3', '0 a 3 kW'),
        ('3-5', '3 a 5 kW'),
        ('5-10', '5 a 10 kW'),
        ('10+', 'Más de 10 kW'),
    ]
    
    rango_potencia = models.CharField(
        max_length=10,
        choices=RANGOS_POTENCIA,
        unique=True,
        verbose_name="Rango de Potencia"
    )
    
    potencia_min = models.FloatField(
        verbose_name="Potencia Mínima (kW)",
        help_text="Potencia mínima del rango en kW"
    )
    
    potencia_max = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Potencia Máxima (kW)",
        help_text="Potencia máxima del rango en kW (dejar vacío para 'más de X')"
    )
    
    costo_por_kw = models.FloatField(
        verbose_name="Costo por kW (USD)",
        help_text="Costo de instalación por kW en este rango"
    )
    
    costo_bateria_por_kw = models.FloatField(
        default=650,
        verbose_name="Costo Batería por kW (USD)",
        help_text="Costo adicional por kW para sistema de baterías"
    )
    
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Descripción adicional del rango de instalación"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Costo de Instalación"
        verbose_name_plural = "Costos de Instalación"
        ordering = ['potencia_min']
    
    def __str__(self):
        if self.potencia_max:
            return f"{self.potencia_min}-{self.potencia_max} kW: ${self.costo_por_kw}/kW"
        else:
            return f"+{self.potencia_min} kW: ${self.costo_por_kw}/kW"
    
    @classmethod
    def get_costo_para_potencia(cls, potencia_kw):
        """Obtener el costo por kW para una potencia específica"""
        costos = cls.objects.filter(activo=True).order_by('potencia_min')
        
        for costo in costos:
            if costo.potencia_max:
                if costo.potencia_min <= potencia_kw <= costo.potencia_max:
                    return costo
            else:
                if potencia_kw >= costo.potencia_min:
                    return costo
        
        # Si no se encuentra, devolver el primer rango
        return costos.first()


class FactorUbicacion(models.Model):
    """Factores de irradiación solar por provincia argentina"""
    
    PROVINCIAS_ARGENTINA = [
        ('caba', 'Ciudad Autónoma de Buenos Aires'),
        ('buenos_aires', 'Buenos Aires'),
        ('catamarca', 'Catamarca'),
        ('chaco', 'Chaco'),
        ('chubut', 'Chubut'),
        ('cordoba', 'Córdoba'),
        ('corrientes', 'Corrientes'),
        ('entre_rios', 'Entre Ríos'),
        ('formosa', 'Formosa'),
        ('jujuy', 'Jujuy'),
        ('la_pampa', 'La Pampa'),
        ('la_rioja', 'La Rioja'),
        ('mendoza', 'Mendoza'),
        ('misiones', 'Misiones'),
        ('neuquen', 'Neuquén'),
        ('rio_negro', 'Río Negro'),
        ('salta', 'Salta'),
        ('san_juan', 'San Juan'),
        ('san_luis', 'San Luis'),
        ('santa_cruz', 'Santa Cruz'),
        ('santa_fe', 'Santa Fe'),
        ('santiago_del_estero', 'Santiago del Estero'),
        ('tierra_del_fuego', 'Tierra del Fuego'),
        ('tucuman', 'Tucumán'),
    ]
    
    provincia = models.CharField(
        max_length=50,
        choices=PROVINCIAS_ARGENTINA,
        unique=True,
        verbose_name="Provincia"
    )
    
    factor_irradiacion = models.FloatField(
        verbose_name="Factor de Irradiación",
        help_text="Factor multiplicador de irradiación (1.0 = promedio nacional)"
    )
    
    irradiacion_promedio = models.FloatField(
        verbose_name="Irradiación Promedio (kWh/m²/día)",
        help_text="Irradiación solar promedio diaria"
    )
    
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Información adicional sobre la irradiación en esta provincia"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Factor de Ubicación"
        verbose_name_plural = "Factores de Ubicación"
        ordering = ['provincia']
    
    def __str__(self):
        return f"{self.get_provincia_display()}: {self.factor_irradiacion}"
    
    @classmethod
    def get_factor_provincia(cls, provincia_code):
        """Obtener factor de irradiación para una provincia"""
        try:
            factor = cls.objects.get(provincia=provincia_code, activo=True)
            return factor.factor_irradiacion
        except cls.DoesNotExist:
            return 0.9  # Factor por defecto


class FactorOrientacion(models.Model):
    """Factores de eficiencia por orientación del tejado"""
    
    ORIENTACIONES = [
        ('N', 'Norte'),
        ('NE', 'Noreste'),
        ('E', 'Este'),
        ('SE', 'Sureste'),
        ('S', 'Sur'),
        ('SO', 'Suroeste'),
        ('O', 'Oeste'),
        ('NO', 'Noroeste'),
    ]
    
    orientacion = models.CharField(
        max_length=2,
        choices=ORIENTACIONES,
        unique=True,
        verbose_name="Orientación"
    )
    
    factor_eficiencia = models.FloatField(
        verbose_name="Factor de Eficiencia",
        help_text="Factor de eficiencia por orientación (1.0 = 100% eficiencia)"
    )
    
    angulo_solar = models.IntegerField(
        verbose_name="Ángulo Solar (grados)",
        help_text="Ángulo respecto al norte (0° = Norte)"
    )
    
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Factor de Orientación"
        verbose_name_plural = "Factores de Orientación"
        ordering = ['angulo_solar']
    
    def __str__(self):
        return f"{self.get_orientacion_display()}: {int(self.factor_eficiencia * 100)}%"
    
    @classmethod
    def get_factor_orientacion(cls, orientacion_code):
        """Obtener factor de eficiencia para una orientación"""
        try:
            factor = cls.objects.get(orientacion=orientacion_code, activo=True)
            return factor.factor_eficiencia
        except cls.DoesNotExist:
            return 0.9  # Factor por defecto


class TipoTejado(models.Model):
    """Tipos de tejado con sus factores de instalación"""
    
    TIPOS_TEJADO = [
        ('plano', 'Techo Plano'),
        ('un_agua', 'Techo a Un Agua'),
        ('dos_aguas', 'Techo a Dos Aguas'),
        ('cuatro_aguas', 'Techo a Cuatro Aguas'),
    ]
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_TEJADO,
        unique=True,
        verbose_name="Tipo de Tejado"
    )
    
    factor_complejidad = models.FloatField(
        default=1.0,
        verbose_name="Factor de Complejidad",
        help_text="Factor que afecta el costo de instalación (1.0 = sin incremento)"
    )
    
    angulo_optimo = models.IntegerField(
        verbose_name="Ángulo Óptimo (grados)",
        help_text="Ángulo de inclinación óptimo para este tipo de tejado"
    )
    
    imagen_svg = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nombre Imagen SVG",
        help_text="Nombre del archivo SVG (ej: tejado-plano.svg)"
    )
    
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Tipo de Tejado"
        verbose_name_plural = "Tipos de Tejado"
        ordering = ['tipo']
    
    def __str__(self):
        return self.get_tipo_display()


class AnguloTejado(models.Model):
    """Ángulos de inclinación predefinidos para tejados"""
    
    angulo = models.IntegerField(
        unique=True,
        verbose_name="Ángulo (grados)"
    )
    
    factor_eficiencia = models.FloatField(
        verbose_name="Factor de Eficiencia",
        help_text="Factor de eficiencia para este ángulo (1.0 = óptimo)"
    )
    
    imagen_svg = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nombre Imagen SVG",
        help_text="Nombre del archivo SVG (ej: angulo-30.svg)"
    )
    
    descripcion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Descripción",
        help_text="Descripción del ángulo (ej: 'Óptimo para Argentina')"
    )
    
    recomendado = models.BooleanField(
        default=False,
        verbose_name="Ángulo Recomendado",
        help_text="Marcar si es el ángulo más recomendado"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Ángulo de Tejado"
        verbose_name_plural = "Ángulos de Tejado"
        ordering = ['angulo']
    
    def __str__(self):
        recomendado = " ⭐" if self.recomendado else ""
        return f"{self.angulo}°{recomendado}"
    
    def get_factor_inclinacion(self):
        """Calcula el factor de eficiencia por inclinación"""
        # El ángulo óptimo para Argentina es alrededor de 32°
        angulo_optimo = 32
        diferencia = abs(self.angulo - angulo_optimo)
        # Factor decrece 1% por cada grado de diferencia
        factor = max(0.7, 1.0 - (diferencia * 0.01))
        return factor