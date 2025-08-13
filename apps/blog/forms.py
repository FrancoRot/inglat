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
                'placeholder': 'https://www.youtube.com/watch?v=abc123 o https://vimeo.com/123456789',
                'size': 100,
                'class': 'vLargeTextField'
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
            "Soportamos: YouTube, Vimeo, Google Drive, Dropbox y URLs directas MP4. "
            "El sistema detectara automaticamente la plataforma y generara las URLs de embed."
        )
        
        self.fields['tipo_multimedia'].help_text = (
            "Selecciona 'imagen' para usar imagen o 'video' para usar video. "
            "Si seleccionas video, asegurate de proporcionar una URL valida."
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
        imagen = cleaned_data.get('imagen')
        video_url = cleaned_data.get('video_url')
        video_vimeo_url = cleaned_data.get('video_vimeo_url')
        
        # Validación de multimedia
        if tipo_multimedia == 'imagen':
            if not imagen:
                raise ValidationError("Debes subir una imagen cuando seleccionas 'imagen' como tipo multimedia")
            if video_url or video_vimeo_url:
                self.add_error('tipo_multimedia', "No puedes tener imagen Y video. Selecciona solo uno.")
        
        elif tipo_multimedia == 'video':
            if not video_url and not video_vimeo_url:
                raise ValidationError("Debes proporcionar una URL de video cuando seleccionas 'video' como tipo multimedia")
            if imagen:
                self.add_error('tipo_multimedia', "No puedes tener imagen Y video. Selecciona solo uno.")
        
        return cleaned_data
    
    def clean_video_url(self):
        """Validación personalizada para la URL de video"""
        video_url = self.cleaned_data.get('video_url')
        
        if not video_url:
            return video_url
        
        # Validar que la URL sea soportada
        try:
            VideoURLValidator.validate_video_url(video_url)
        except ValidationError as e:
            raise ValidationError(f"URL de video invalida: {str(e)}")
        
        # Verificar que sea accesible solo si requests está disponible
        tipo_multimedia = self.cleaned_data.get('tipo_multimedia')
        if tipo_multimedia == 'video' and HAS_REQUESTS:
            platform = VideoURLValidator.detect_platform(video_url)
            if not VideoURLValidator.test_video_accessibility(video_url, platform):
                self.add_error('video_url', 
                    "Advertencia: No se pudo verificar que el video sea accesible publicamente. "
                    "Asegurate de que el enlace no requiera autenticacion."
                )
        
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