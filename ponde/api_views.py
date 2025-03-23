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

from django_q.tasks import async_task
from django.http import JsonResponse
from django_q.models import OrmQ

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
        
def ejecucion_tareas(request):
    if request.method == 'POST':
        func = 'ponde.services.explore_linkedin_ad'
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'error': 'Error en el JSON'}, status=400)
        
        print('data:', data)

        url_anuncio = data.get('url_oferta')
        username = data.get('email_acceso')
        password = data.get('contraseña_acceso')

        task_name = f"linkedin_ad_{url_anuncio.replace('https://www.linkedin.com/hiring/jobs/','')[:21]}"

        if not all([url_anuncio, username, password]):
            return JsonResponse({'error': 'Faltan parámetros'}, status=400)

        tasks = [obj.func() for obj in OrmQ.objects.all()]
        if func not in tasks:
            task_id = async_task(func, url_anuncio, username, password, task_name=task_name)
            print(f'Se asigno nueva tarea con id: {task_id} y func: {func}')
        else:
            print('Ya existe la tarea')

        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)