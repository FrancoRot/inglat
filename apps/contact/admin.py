from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin para gestionar mensajes de contacto"""
    
    list_display = [
        'nombre', 
        'email', 
        'telefono', 
        'tipo_proyecto', 
        'fecha_creacion', 
        'leido', 
        'respondido'
    ]
    
    list_filter = [
        'tipo_proyecto', 
        'leido', 
        'respondido', 
        'fecha_creacion'
    ]
    
    search_fields = [
        'nombre', 
        'email', 
        'telefono', 
        'mensaje'
    ]
    
    readonly_fields = [
        'fecha_creacion', 
        'ip_address'
    ]
    
    fieldsets = (
        ('Informacion del Cliente', {
            'fields': ('nombre', 'email', 'telefono')
        }),
        ('Proyecto', {
            'fields': ('tipo_proyecto', 'mensaje')
        }),
        ('Control Interno', {
            'fields': ('leido', 'respondido', 'notas_internas')
        }),
        ('Metadata', {
            'fields': ('fecha_creacion', 'ip_address'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['marcar_como_leido', 'marcar_como_respondido']
    
    def marcar_como_leido(self, request, queryset):
        """Accion para marcar mensajes como leidos"""
        updated = queryset.update(leido=True)
        self.message_user(
            request,
            f'{updated} mensaje(s) marcado(s) como leido(s).'
        )
    marcar_como_leido.short_description = "Marcar como leido"
    
    def marcar_como_respondido(self, request, queryset):
        """Accion para marcar mensajes como respondidos"""
        updated = queryset.update(respondido=True, leido=True)
        self.message_user(
            request,
            f'{updated} mensaje(s) marcado(s) como respondido(s).'
        )
    marcar_como_respondido.short_description = "Marcar como respondido"
    
    def get_queryset(self, request):
        """Ordenar por fecha de creacion descendente"""
        return super().get_queryset(request).order_by('-fecha_creacion')