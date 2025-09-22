from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Lista temporal de proyectos - placeholder
    path('', views.project_list, name='list'),
    
    # Detalle de proyecto usando slug
    path('<slug:slug>/', views.project_detail, name='detail'),
]