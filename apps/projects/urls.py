from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Lista temporal de proyectos - placeholder
    path('', views.project_list, name='list'),
    
    # Detalle de proyecto - placeholder  
    path('<int:pk>/', views.project_detail, name='detail'),
]