import json
from datetime import datetime
import time
import pandas as pd
import logging

from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

""" from decimal import Decimal
from datetime import date
from django.http import JsonResponse
from django.db.models import Q
from django.views import View """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class OfertasLaboralesViewSet(viewsets.ModelViewSet):
    queryset = OfertasLaborales.objects.all()
    serializer_class = OfertasLaboralesSerializer


class CandidatosPorOfertaAPIView(APIView):
    def get(self, request, id_oferta_laboral):
        try:
            # Verificar si la oferta laboral existe
            oferta = OfertasLaborales.objects.get(id=id_oferta_laboral)
            
            # Obtener los candidatos asociados a la oferta
            candidatos = Candidatos.objects.filter(id_oferta_laboral=oferta)

            # Construir el JSON de respuesta
            response_data = {}
            for candidato in candidatos:
                ponderado = Ponderado.objects.filter(id_candidato=candidato).first()
                
                response_data[candidato.id_candidato] = {
                    "info": CandidatosSerializer(candidato).data,
                    "ponde": PonderadoSerializer(ponderado).data if ponderado else None
                }

            return Response(response_data, status=status.HTTP_200_OK)
        
        except OfertasLaborales.DoesNotExist:
            return Response({"error": "La oferta laboral no existe."}, status=status.HTTP_404_NOT_FOUND)