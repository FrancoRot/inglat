from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Lista principal de noticias
    path('', views.NoticiasListView.as_view(), name='lista'),
    
    # Filtrado AJAX de noticias
    path('filtrar/', views.filtrar_noticias_ajax, name='filtrar_ajax'),
    
    # Noticias por categoría
    path('categoria/<slug:categoria_slug>/', views.NoticiasPorCategoriaView.as_view(), name='por_categoria'),
    
    # Detalle de noticia (slug SEO-friendly)
    path('<slug:slug>/', views.NoticiaDetailView.as_view(), name='detalle'),
    
    # URLs de compatibilidad (mantener funcionalidad existente)
    path('list/', views.blog_list, name='list_compat'),
    path('detail/<int:pk>/', views.blog_detail, name='detail_compat'),
]