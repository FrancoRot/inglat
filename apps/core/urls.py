from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Página de inicio - usando vista función
    path('', views.index, name='home'),
    
    # Página de inicio alternativa - usando vista basada en clase
    # path('', views.HomeView.as_view(), name='home'),
    
    # Página Nosotros
    path('nosotros/', views.AboutView.as_view(), name='about'),
    
    # Página Servicios
    path('servicios/', views.ServicesView.as_view(), name='services'),
]