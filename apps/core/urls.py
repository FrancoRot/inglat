from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # P�gina de inicio - usando vista funci�n
    path('', views.index, name='home'),
    
    # P�gina de inicio alternativa - usando vista basada en clase
    # path('', views.HomeView.as_view(), name='home'),
    
    # P�gina Nosotros
    path('nosotros/', views.AboutView.as_view(), name='about'),
    
    # P�gina Servicios
    path('servicios/', views.ServicesView.as_view(), name='services'),
]