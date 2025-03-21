from rest_framework import serializers
from .models import *

class OfertasLaboralesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertasLaborales
        fields = '__all__' 

class CandidatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidatos
        fields = '__all__'

class PonderadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ponderado
        fields = '__all__'