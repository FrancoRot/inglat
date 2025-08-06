from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    # Página de contacto principal
    path('', views.ContactView.as_view(), name='contact'),
    
    # Página de éxito después del envío
    path('enviado/', views.contact_success, name='contact_success'),
]