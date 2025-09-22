# -*- coding: utf-8 -*-
"""
Formularios personalizados para el blog de INGLAT
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Noticia, Categoria
from .utils import VideoURLValidator, HAS_REQUESTS


class NoticiaAdminForm(forms.ModelForm):
    """Formulario personalizado para el admin de Noticia con validación de videos"""
    
    class Meta:
        model = Noticia
        fields = '__all__'
        widgets = {
            'video_url': forms.URLInput(attrs={
                'placeholder': 'https://www.youtube.com/watch?v=abc123 o https://example.com/imagen.jpg',
                'size': 100,
                'class': 'vLargeTextField'
            }),
            'archivo': forms.FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.gif,.mp4,.webm,.mov,.avi,.m4v'
            }),
            'contenido': forms.Textarea(attrs={
                'rows': 20,
                'cols': 100
            }),
            'descripcion_corta': forms.Textarea(attrs={
                'rows': 3,
                'cols': 100
            }),
            'meta_descripcion': forms.Textarea(attrs={
                'rows': 2,
                'cols': 100
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Agregar ayuda contextual
        self.fields['video_url'].help_text = (
            "URLs soportadas: YouTube, Vimeo, Google Drive, Dropbox y URLs directas de archivos. "
            "El sistema detectara automaticamente la plataforma y generara las URLs de embed."
        )
        
        self.fields['archivo'].help_text = (
            "Sube un archivo directamente: JPG/PNG para imagenes, MP4/WebM para videos. "
            "Maximo 50MB por archivo."
        )
        
        self.fields['tipo_multimedia'].help_text = (
            "Selecciona el tipo de contenido. Las opciones de configuracion cambian dinamicamente."
        )
        
        self.fields['thumbnail_custom'].help_text = (
            "Miniatura personalizada (opcional). Se usara en las tarjetas en lugar de la miniatura automatica."
        )
        
        # Hacer campos readonly cuando corresponda (verificar existencia primero)
        if self.instance.pk:
            readonly_fields = ['video_platform', 'video_id', 'video_embed_url_cached', 'video_thumbnail_url']
            for field_name in readonly_fields:
                if field_name in self.fields:
                    self.fields[field_name].widget.attrs['readonly'] = True
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_multimedia = cleaned_data.get('tipo_multimedia')
        archivo = cleaned_data.get('archivo')
        video_url = cleaned_data.get('video_url')
        
        # Validación de multimedia
        if tipo_multimedia == 'imagen':
            if not archivo and not video_url:
                raise ValidationError("Debes subir un archivo o proporcionar una URL cuando seleccionas 'imagen'")
            
            # Validar tipo de archivo si se sube
            if archivo:
                import os
                ext = os.path.splitext(archivo.name)[1].lower()
                image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
                if ext not in image_extensions:
                    self.add_error('archivo', f"Para imagenes solo se permiten archivos: {', '.join(image_extensions)}")
        
        elif tipo_multimedia == 'video':
            if not archivo and not video_url:
                raise ValidationError("Debes subir un archivo o proporcionar una URL cuando seleccionas 'video'")
            
            # Validar tipo de archivo si se sube
            if archivo:
                import os
                ext = os.path.splitext(archivo.name)[1].lower()
                video_extensions = ['.mp4', '.webm', '.mov', '.avi', '.m4v']
                if ext not in video_extensions:
                    self.add_error('archivo', f"Para videos solo se permiten archivos: {', '.join(video_extensions)}")
        
        # Validar que no se use archivo y URL al mismo tiempo
        if archivo and video_url:
            self.add_error('video_url', "No puedes usar archivo y URL al mismo tiempo. Selecciona solo uno.")
            self.add_error('archivo', "No puedes usar archivo y URL al mismo tiempo. Selecciona solo uno.")
        
        return cleaned_data
    
    def clean_video_url(self):
        """Validación personalizada para la URL multimedia"""
        video_url = self.cleaned_data.get('video_url')
        
        if not video_url:
            return video_url
        
        tipo_multimedia = self.cleaned_data.get('tipo_multimedia')
        
        # Para videos, validar que la URL sea soportada
        if tipo_multimedia == 'video':
            try:
                VideoURLValidator.validate_video_url(video_url)
            except ValidationError as e:
                raise ValidationError(f"URL de video invalida: {str(e)}")
            
            # Verificar que sea accesible solo si requests está disponible
            if HAS_REQUESTS:
                platform = VideoURLValidator.detect_platform(video_url)
                if not VideoURLValidator.test_video_accessibility(video_url, platform):
                    self.add_error('video_url', 
                        "Advertencia: No se pudo verificar que el video sea accesible publicamente. "
                        "Asegurate de que el enlace no requiera autenticacion."
                    )
        
        # Para imágenes, hacer validación básica de URL
        elif tipo_multimedia == 'imagen':
            # Verificar que sea una URL válida
            from django.core.validators import URLValidator
            url_validator = URLValidator()
            try:
                url_validator(video_url)
            except ValidationError:
                raise ValidationError("Formato de URL inválido para imagen")
        
        return video_url


class VideoURLTestForm(forms.Form):
    """Formulario para testing de URLs de video en el admin"""
    
    video_url = forms.URLField(
        label="URL de Video",
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.youtube.com/watch?v=abc123',
            'size': 80,
            'class': 'vLargeTextField'
        }),
        help_text="Introduce una URL de video para probar si es compatible"
    )
    
    def clean_video_url(self):
        video_url = self.cleaned_data['video_url']
        
        try:
            VideoURLValidator.validate_video_url(video_url)
        except ValidationError as e:
            raise ValidationError(f"URL no valida: {str(e)}")
        
        return video_url
    
    def get_video_info(self):
        """Retorna información del video para mostrar en el admin"""
        if not hasattr(self, 'cleaned_data') or 'video_url' not in self.cleaned_data:
            return None
        
        video_url = self.cleaned_data['video_url']
        platform = VideoURLValidator.detect_platform(video_url)
        video_id = VideoURLValidator.extract_video_id(video_url, platform)
        embed_url = VideoURLValidator.get_embed_url(video_url, platform)
        thumbnail_url = VideoURLValidator.get_thumbnail_url(video_url, platform)
        is_accessible = False
        
        if HAS_REQUESTS:
            is_accessible = VideoURLValidator.test_video_accessibility(video_url, platform)
        
        return {
            'url': video_url,
            'platform': platform,
            'video_id': video_id,
            'embed_url': embed_url,
            'thumbnail_url': thumbnail_url,
            'is_accessible': is_accessible
        }