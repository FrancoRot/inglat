from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    # Página de contacto - placeholder
    path('', views.contact, name='contact'),
]