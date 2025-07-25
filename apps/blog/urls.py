from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Lista temporal de blog - placeholder
    path('', views.blog_list, name='list'),
    
    # Detalle de post - placeholder
    path('<int:pk>/', views.blog_detail, name='detail'),
]