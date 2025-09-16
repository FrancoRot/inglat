/**
 * JavaScript para el admin de noticias - Control dinámico de campos multimedia
 */

(function($) {
    'use strict';

    // Función para mostrar/ocultar campos según el tipo de multimedia
    function toggleMultimediaFields() {
        var tipoMultimedia = $('#id_tipo_multimedia').val();
        
        // Elementos de video
        var videoControls = $('.field-video_autoplay, .field-video_muted, .field-video_loop, .field-video_show_controls').parent();
        
        // Mostrar/ocultar según el tipo
        if (tipoMultimedia === 'video') {
            videoControls.show();
            
            // Mostrar mensaje de ayuda para videos
            if (!$('#video-help-text').length) {
                $('#id_archivo').after(
                    '<div id="video-help-text" class="help" style="color: #006466; font-weight: bold;">' +
                    '📹 Modo Video: Sube un archivo MP4/WebM o usa una URL de video' +
                    '</div>'
                );
            }
            
            if (!$('#imagen-help-text').length) {
                // Quitar mensaje de imagen si existe
                $('#imagen-help-text').remove();
            }
            
        } else if (tipoMultimedia === 'imagen') {
            videoControls.hide();
            
            // Mostrar mensaje de ayuda para imágenes
            if (!$('#imagen-help-text').length) {
                $('#id_archivo').after(
                    '<div id="imagen-help-text" class="help" style="color: #006466; font-weight: bold;">' +
                    '🖼️ Modo Imagen: Sube un archivo JPG/PNG o usa una URL de imagen' +
                    '</div>'
                );
            }
            
            if (!$('#video-help-text').length) {
                // Quitar mensaje de video si existe
                $('#video-help-text').remove();
            }
            
        } else { // ninguno
            videoControls.hide();
            $('#video-help-text, #imagen-help-text').remove();
        }
    }

    // Función para preview inmediato de archivos
    function setupFilePreview() {
        $('#id_archivo').change(function() {
            var file = this.files[0];
            if (file) {
                var reader = new FileReader();
                var tipoMultimedia = $('#id_tipo_multimedia').val();
                
                reader.onload = function(e) {
                    // Remover preview anterior
                    $('#file-preview').remove();
                    
                    var previewHtml = '<div id="file-preview" style="margin-top: 10px; padding: 10px; border: 2px solid #006466; border-radius: 4px; background: #f9f9f9;">';
                    previewHtml += '<h4>📁 Vista Previa del Archivo:</h4>';
                    
                    if (tipoMultimedia === 'imagen' && file.type.startsWith('image/')) {
                        previewHtml += '<img src="' + e.target.result + '" style="max-width: 300px; max-height: 200px; border-radius: 4px;" />';
                    } else if (tipoMultimedia === 'video' && file.type.startsWith('video/')) {
                        previewHtml += '<video width="300" height="200" controls><source src="' + e.target.result + '" type="' + file.type + '">Tu navegador no soporta video HTML5.</video>';
                    }
                    
                    previewHtml += '<p><strong>Archivo:</strong> ' + file.name + ' (' + Math.round(file.size/1024) + ' KB)</p>';
                    previewHtml += '</div>';
                    
                    $('#id_archivo').after(previewHtml);
                };
                
                reader.readAsDataURL(file);
            } else {
                $('#file-preview').remove();
            }
        });
    }

    // Función para preview inmediato de URLs
    function setupURLPreview() {
        $('#id_video_url').blur(function() {
            var url = $(this).val();
            if (url) {
                // Remover preview anterior
                $('#url-preview').remove();
                
                var previewHtml = '<div id="url-preview" style="margin-top: 10px; padding: 10px; border: 2px solid #008B8D; border-radius: 4px; background: #f0f9f9;">';
                previewHtml += '<h4>🔗 Vista Previa de URL:</h4>';
                previewHtml += '<p><strong>URL:</strong> <a href="' + url + '" target="_blank">' + url + '</a></p>';
                
                // Detectar tipo de plataforma
                if (url.includes('youtube.com') || url.includes('youtu.be')) {
                    previewHtml += '<p>📺 <strong>Plataforma:</strong> YouTube</p>';
                } else if (url.includes('vimeo.com')) {
                    previewHtml += '<p>📺 <strong>Plataforma:</strong> Vimeo</p>';
                } else if (url.includes('drive.google.com')) {
                    previewHtml += '<p>💾 <strong>Plataforma:</strong> Google Drive</p>';
                } else if (url.includes('dropbox.com')) {
                    previewHtml += '<p>💾 <strong>Plataforma:</strong> Dropbox</p>';
                } else {
                    previewHtml += '<p>🔗 <strong>Plataforma:</strong> URL Directa</p>';
                }
                
                previewHtml += '<p><small><em>La información detallada se generará al guardar</em></small></p>';
                previewHtml += '</div>';
                
                $(this).after(previewHtml);
            } else {
                $('#url-preview').remove();
            }
        });
    }

    // Función para validar que no se usen archivo y URL al mismo tiempo
    function setupMutualExclusion() {
        $('#id_archivo').change(function() {
            if (this.files && this.files[0]) {
                $('#id_video_url').val('').trigger('blur');
                $('#url-preview').remove();
            }
        });

        $('#id_video_url').blur(function() {
            if ($(this).val()) {
                $('#id_archivo').val('');
                $('#file-preview').remove();
            }
        });
    }

    // Inicializar cuando el documento esté listo
    $(document).ready(function() {
        // Solo ejecutar en páginas del admin de noticias
        if ($('#id_tipo_multimedia').length) {
            console.log('Inicializando JavaScript multimedia admin...');
            
            // Configurar el toggle inicial
            toggleMultimediaFields();
            
            // Configurar event listeners
            $('#id_tipo_multimedia').change(toggleMultimediaFields);
            setupFilePreview();
            setupURLPreview();
            setupMutualExclusion();
            
            // Mostrar instrucciones iniciales
            if (!$('.multimedia-instructions').length) {
                $('#id_tipo_multimedia').after(
                    '<div class="multimedia-instructions help" style="background: #e8f4fd; padding: 10px; border-radius: 4px; margin: 10px 0;">' +
                    '<strong>💡 Instrucciones:</strong><br>' +
                    '• <strong>Archivo</strong>: Sube directamente JPG/PNG (imágenes) o MP4/WebM (videos)<br>' +
                    '• <strong>URL</strong>: Enlaza desde YouTube, Vimeo, Drive, Dropbox, etc.<br>' +
                    '• Solo puedes usar <strong>archivo</strong> O <strong>URL</strong>, no ambos<br>' +
                    '• La miniatura personalizada es opcional y se usa en las tarjetas' +
                    '</div>'
                );
            }
            
            console.log('JavaScript multimedia admin inicializado correctamente');
        }
    });

})(django.jQuery);