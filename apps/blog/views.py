from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Noticia, Categoria


class NoticiasListView(ListView):
    """Vista principal para la lista de noticias"""
    model = Noticia
    template_name = 'blog/noticias_lista.html'
    context_object_name = 'noticias'
    paginate_by = None  # Sin paginación según requerimientos
    
    def get_queryset(self):
        """Filtra noticias activas con relaciones optimizadas"""
        queryset = Noticia.objects.filter(
            activa=True
        ).select_related('categoria').order_by('-fecha_publicacion', 'orden')
        
        # Filtro por categoría
        categoria_slug = self.request.GET.get('categoria')
        if categoria_slug and categoria_slug != 'todas':
            queryset = queryset.filter(categoria__slug=categoria_slug)
        
        # Filtro por fecha
        fecha_filtro = self.request.GET.get('fecha')
        if fecha_filtro and fecha_filtro != 'todas':
            if fecha_filtro == 'este-mes':
                from django.utils import timezone
                import datetime
                ahora = timezone.now()
                inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                queryset = queryset.filter(fecha_publicacion__gte=inicio_mes)
            elif fecha_filtro == 'ultimo-mes':
                from django.utils import timezone
                import datetime
                ahora = timezone.now()
                hace_un_mes = ahora - datetime.timedelta(days=30)
                queryset = queryset.filter(fecha_publicacion__gte=hace_un_mes)
        
        # Búsqueda por texto
        busqueda = self.request.GET.get('q')
        if busqueda:
            queryset = queryset.filter(
                Q(titulo__icontains=busqueda) | 
                Q(descripcion_corta__icontains=busqueda) |
                Q(contenido__icontains=busqueda)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Añade contexto adicional"""
        context = super().get_context_data(**kwargs)
        
        # Todas las categorías activas para el filtro
        context['categorias'] = Categoria.objects.filter(activa=True)
        
        # Filtros actuales para mantener estado
        filtro_categoria = self.request.GET.get('categoria', 'todas')
        context['filtro_categoria'] = filtro_categoria
        context['filtro_fecha'] = self.request.GET.get('fecha', 'todas')
        context['filtro_busqueda'] = self.request.GET.get('q', '')
        
        # Categoría actual filtrada (si hay filtro específico)
        context['categoria_actual'] = None
        if filtro_categoria and filtro_categoria != 'todas':
            try:
                context['categoria_actual'] = Categoria.objects.get(
                    slug=filtro_categoria, activa=True
                )
            except Categoria.DoesNotExist:
                pass
        
        # Noticias destacadas para sidebar
        context['noticias_destacadas'] = Noticia.objects.filter(
            destacada=True,
            activa=True
        )[:3]
        
        # Categorías con conteo para sidebar
        categorias_con_conteo = []
        for categoria in context['categorias']:
            categoria.noticias_count_activas = categoria.noticia_set.filter(activa=True).count()
            categorias_con_conteo.append(categoria)
        context['categorias_con_conteo'] = categorias_con_conteo
        
        return context


class NoticiaDetailView(DetailView):
    """Vista para el detalle de una noticia"""
    model = Noticia
    template_name = 'blog/noticia_detalle.html'
    context_object_name = 'noticia'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Solo noticias activas con relaciones optimizadas"""
        return Noticia.objects.filter(activa=True).select_related('categoria')
    
    def get_context_data(self, **kwargs):
        """Añade contexto adicional"""
        context = super().get_context_data(**kwargs)
        
        # Noticias relacionadas de la misma categoría
        if self.object.categoria:
            context['noticias_relacionadas'] = Noticia.objects.filter(
                categoria=self.object.categoria,
                activa=True
            ).exclude(pk=self.object.pk)[:3]
        else:
            context['noticias_relacionadas'] = []
        
        # Breadcrumbs
        context['breadcrumbs'] = [
            {'name': 'Inicio', 'url': '/'},
            {'name': 'Noticias', 'url': '/noticias/'},
            {'name': self.object.titulo, 'url': None}  # Actual, sin URL
        ]
        
        # Schema markup para SEO
        context['schema_markup'] = self.get_schema_markup()
        
        return context
    
    def get_schema_markup(self):
        """Genera schema markup JSON-LD para la noticia"""
        import json
        from django.urls import reverse
        
        schema = {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": self.object.titulo,
            "description": self.object.descripcion_corta,
            "datePublished": self.object.fecha_publicacion.isoformat(),
            "dateModified": self.object.fecha_actualizacion.isoformat(),
            "author": {
                "@type": "Organization",
                "name": self.object.autor
            },
            "publisher": {
                "@type": "Organization",
                "name": "INGLAT",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://inglat.com/static/images/logo/inglat-logo.png"
                }
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": self.request.build_absolute_uri()
            }
        }
        
        # Añadir imagen si existe (usando el campo archivo para imágenes o thumbnail_custom)
        thumbnail_url = self.object.get_thumbnail_url()
        if thumbnail_url:
            schema["image"] = self.request.build_absolute_uri(thumbnail_url)
        elif self.object.archivo and self.object.tipo_multimedia == 'imagen':
            schema["image"] = self.request.build_absolute_uri(self.object.archivo.url)
        
        # Añadir video si existe
        if self.object.video_embed_url:
            schema["video"] = {
                "@type": "VideoObject",
                "embedUrl": self.object.video_embed_url,
                "name": self.object.titulo,
                "description": self.object.descripcion_corta
            }
        
        return json.dumps(schema, indent=2)


class NoticiasPorCategoriaView(ListView):
    """Vista para noticias filtradas por categoría"""
    model = Noticia
    template_name = 'blog/noticias_categoria.html'
    context_object_name = 'noticias'
    paginate_by = None
    
    def get_queryset(self):
        """Filtra noticias por categoría"""
        self.categoria = get_object_or_404(
            Categoria, 
            slug=self.kwargs['categoria_slug'], 
            activa=True
        )
        
        return Noticia.objects.filter(
            categoria=self.categoria,
            activa=True
        ).select_related('categoria').order_by('-fecha_publicacion')
    
    def get_context_data(self, **kwargs):
        """Añade contexto adicional"""
        context = super().get_context_data(**kwargs)
        context['categoria_actual'] = self.categoria
        context['categorias'] = Categoria.objects.filter(activa=True)
        
        # Breadcrumbs
        context['breadcrumbs'] = [
            {'name': 'Inicio', 'url': '/'},
            {'name': 'Noticias', 'url': '/noticias/'},
            {'name': self.categoria.nombre, 'url': None}
        ]
        
        return context


def filtrar_noticias_ajax(request):
    """Vista AJAX para filtrado dinámico de noticias"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Solo peticiones AJAX'}, status=400)
    
    # Obtener parámetros
    categoria_slug = request.GET.get('categoria', 'todas')
    fecha_filtro = request.GET.get('fecha', 'todas')
    busqueda = request.GET.get('q', '')
    
    # Construir queryset
    queryset = Noticia.objects.filter(activa=True).select_related('categoria')
    
    # Aplicar filtros
    if categoria_slug != 'todas':
        queryset = queryset.filter(categoria__slug=categoria_slug)
    
    if fecha_filtro != 'todas':
        from django.utils import timezone
        import datetime
        ahora = timezone.now()
        
        if fecha_filtro == 'este-mes':
            inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            queryset = queryset.filter(fecha_publicacion__gte=inicio_mes)
        elif fecha_filtro == 'ultimo-mes':
            hace_un_mes = ahora - datetime.timedelta(days=30)
            queryset = queryset.filter(fecha_publicacion__gte=hace_un_mes)
    
    if busqueda:
        queryset = queryset.filter(
            Q(titulo__icontains=busqueda) | 
            Q(descripcion_corta__icontains=busqueda)
        )
    
    # Ordenar y limitar
    noticias = queryset.order_by('-fecha_publicacion')[:20]
    
    # Serializar datos
    data = []
    for noticia in noticias:
        data.append({
            'id': noticia.id,
            'titulo': noticia.titulo,
            'descripcion_corta': noticia.descripcion_corta,
            'url': noticia.get_absolute_url(),
            'fecha': noticia.fecha_formateada,
            'categoria': {
                'nombre': noticia.categoria.nombre if noticia.categoria else '',
                'color': noticia.categoria.color if noticia.categoria else '#006466'
            },
            'imagen_url': noticia.imagen_url,
            'tiempo_lectura': noticia.tiempo_lectura
        })
    
    return JsonResponse({
        'noticias': data,
        'total': len(data)
    })


# Views de compatibilidad (mantener URLs existentes)
def blog_list(request):
    """Redirecciona a la nueva vista de lista"""
    from django.shortcuts import redirect
    return redirect('blog:lista')

def blog_detail(request, pk):
    """Vista de compatibilidad para detalle por ID"""
    noticia = get_object_or_404(Noticia, pk=pk, activa=True)
    return redirect('blog:detalle', slug=noticia.slug)