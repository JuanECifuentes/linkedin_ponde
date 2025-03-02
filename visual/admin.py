from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('idCliente','nombre_cliente_enlace','telefono','email','redes_sociales','fecha_registro')
    search_fields = ('nombre_cliente', 'telefono','email')
    readonly_fields = ('updated_by',)  # Esto hace que el campo 'updated_by' sea solo lectura en el admin

    def nombre_cliente_enlace(self, obj):
        # Crea un enlace que redirige a la página de edición del cliente
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html('<a style="font-weight: bold;" href="{}">{}</a>', url, obj.nombre_cliente)
    
    nombre_cliente_enlace.admin_order_field = 'nombre_cliente' 
    nombre_cliente_enlace.short_description = 'Nombre Cliente'  

@admin.register(Ofertas)
class OfertasAdmin(admin.ModelAdmin):
    list_display = ('idOferta','titulo_oferta','salario','ubicacion')