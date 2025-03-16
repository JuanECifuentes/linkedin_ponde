from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
@admin.register(OfertasLaborales)
class OfertasLaboralesAdmin(admin.ModelAdmin):
    list_display = ('id','enlace_oferta','descripcion','fecha_creacion')
    search_fields = ('id', 'enlace_oferta','descripcion')
    readonly_fields = ('fecha_creacion',)  # Esto hace que el campo 'fecha_creacion' sea solo lectura en el admin

@admin.register(Candidatos)
class CandidatosAdmin(admin.ModelAdmin):
    list_display = ('id_candidato','nombre_candidato','ubicacion','enlace_perfil','experiencia','educacion','curriculum','preguntas_preseleccion','id_oferta_laboral')

@admin.register(Ponderado)
class PonderadoAdmin(admin.ModelAdmin):
    list_display = ('id','experiencia_cargo','experiencia_herramienta','nivel_ingles','titulo_academico','id_candidato')