from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone

class OfertasLaborales(models.Model):
    id = models.AutoField(primary_key=True)
    titulo_oferta = models.TextField()
    enlace_oferta = models.TextField(unique=True, blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)
    candidatos_cant = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Oferta {self.id} - {self.titulo_oferta}"
    
    class Meta:
        verbose_name='OfertasLaborales'
        verbose_name_plural='OfertasLaborales'
        db_table = '"Specify"."OfertasLaborales"'

class Candidatos(models.Model):
    id_candidato = models.AutoField(primary_key=True)
    nombre_candidato = models.TextField(blank=False, null=False)
    ubicacion = models.TextField(blank=True, null=True)
    enlace_perfil = models.TextField(blank=True, null=True)
    experiencia = models.JSONField(blank=True, null=True)
    educacion = models.JSONField(blank=True, null=True)
    curriculum = models.TextField(blank=True, null=True)
    preguntas_preseleccion = models.JSONField(blank=True, null=True)
    url_oferta_candidato = models.TextField(blank=True, null=True)
    id_oferta_laboral = models.ForeignKey(OfertasLaborales, on_delete=models.CASCADE, related_name="candidatos")

    def __str__(self):
        return f"{self.nombre_candidato} - Oferta {self.id_oferta_laboral.id}"
    
    class Meta:
        verbose_name='Candidatos'
        verbose_name_plural='Candidatos'
        db_table = '"Specify"."Candidatos"'


class Ponderado(models.Model):
    id = models.AutoField(primary_key=True)
    experiencia_cargo = models.IntegerField(blank=True, null=True)
    experiencia_herramienta = models.IntegerField(blank=True, null=True)
    nivel_ingles = models.IntegerField(blank=True, null=True)
    titulo_academico = models.IntegerField(blank=True, null=True)
    id_candidato = models.ForeignKey(Candidatos, on_delete=models.CASCADE, related_name="ponderado", unique=True)

    def __str__(self):
        return f"{self.id_candidato.nombre_candidato} - Oferta id: {self.id_candidato.id_oferta_laboral.id}"
    
    class Meta:
        verbose_name='Ponderado'
        verbose_name_plural='Ponderado'
        db_table = '"Specify"."Ponderado"'

