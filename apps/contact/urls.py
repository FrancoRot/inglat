from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    # P�gina de contacto - placeholder
    path('', views.contact, name='contact'),
]