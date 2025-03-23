from django.urls import path
from .api_views import *

app_name = 'ponde'
urlpatterns = [
    path('api/ofertas-laborales/', OfertasLaboralesViewSet.as_view({'get': 'list'}), name='ofertas-laborales'),
    path('api/candidatos_por_oferta/<int:id_oferta_laboral>/', CandidatosPorOfertaAPIView.as_view(), name='candidatos_por_oferta'),
    path('ejecucion_tareas', ejecucion_tareas, name='ejecucion_tareas'),
]