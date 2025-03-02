from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Clientes(models.Model):
    idCliente = models.AutoField(db_column='idCliente',primary_key=True)
    nombre_cliente = models.CharField(max_length=100)
    telefono =  models.CharField(
        max_length=15, 
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$',
                message='El número de teléfono debe contener entre 7 y 15 dígitos y puede comenzar con "+"'
            )
        ],
        null=True,
        blank=True,
        unique=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    redes_sociales = models.TextField(null=True,blank=True)
    fecha_registro = models.DateTimeField(auto_created=True,default=datetime.now())

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=False,null=False,auto_now=True)

    def __str__(self):
        return f'{self.nombre_cliente} ({self.idCliente})'
    
    class Meta:
        verbose_name='Clientes'
        verbose_name_plural='Clientes'


class Ofertas(models.Model):
    idOferta = models.AutoField(db_column='idOferta',primary_key=True)
    titulo_oferta = models.TextField()
    salario = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    page = models.CharField(max_length=255)
    captured_at = models.DateTimeField(auto_now=timezone.now())

    def __str__(self):
        return f'{self.titulo_oferta} ({self.idOferta})'
    
    class Meta:
        verbose_name='Ofertas'
        verbose_name_plural='Ofertas'
        unique_together = ('titulo_oferta', 'salario', 'ubicacion')  # Aquí se establece la clave compuesta