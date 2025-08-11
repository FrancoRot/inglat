from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Página de inicio - usando vista basada en clase (mejor práctica)
    path('', views.HomeView.as_view(), name='home'),
    
    
    # Página Servicios
    path('servicios/', views.ServicesView.as_view(), name='services'),
    
    # Simulador Solar
    path('simulador/', views.SimuladorSolarView.as_view(), name='simulador'),
]