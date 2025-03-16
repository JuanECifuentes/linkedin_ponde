import logging
from .models import *
from .bots.commands import *
from django.db import transaction

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_or_update_ofertas(data):
    logging.info('<------------- Init data insert on database ------------>')
    try:
        url_oferta = data['anuncio']['url']
        titulo_oferta = data['anuncio']['cargo'] if data['anuncio']['cargo'] != '' else 'Oferta sin título'
        
        # Verificar si la oferta ya existe
        oferta, creada = OfertasLaborales.objects.get_or_create(
            enlace_oferta=url_oferta,
            defaults={
                'titulo_oferta': titulo_oferta,
                'descripcion': '',  # Puedes agregar más detalles si es necesario
                'candidatos_cant': data['caught'],
            }
        )
        
        
        # Procesar candidatos
        candidatos_data = data.get('process_data', {})
        nuevos_candidatos = []
        
        with transaction.atomic():  # Garantiza consistencia en la BD
            for nombre, detalles in candidatos_data.items():
                if not Candidatos.objects.filter(nombre_candidato=nombre, id_oferta_laboral=oferta, url_oferta_candidato=detalles.get('Link', None)).exists():
                    candidato = Candidatos.objects.create(
                        nombre_candidato=nombre,
                        ubicacion=detalles.get('Ubicacion', None),
                        enlace_perfil=detalles.get('Enlace perfil', None),
                        experiencia=detalles.get('Experiencia', {}),
                        educacion=detalles.get('Educacion', {}),
                        curriculum=detalles.get('Curriculum', None),
                        preguntas_preseleccion=detalles.get('Preseleccion', {}),
                        url_oferta_candidato=detalles.get('Link', None),
                        id_oferta_laboral=oferta
                    )
                    nuevos_candidatos.append(candidato)
        
        # Actualizar cantidad de candidatos en la oferta
        oferta.candidatos_cant = data['caught']
        oferta.save()
        
        return {
            "status": "success",
            "oferta_creada": creada,
            "nuevos_candidatos_count": len(nuevos_candidatos),
            "nuevos_candidatos_list": nuevos_candidatos
        }
    except Exception as e:
        logging.error(f'Error al insertar en bd: {e}')
        return {
            "status": "Error",
        }
    
def var_assigns(var, score : int):
    if var == None:
        var = score
    else:
        var = (var + score)/ 2

    return var

def numerical_calculator(var, respuestas):
    respuesta_ideal = respuestas['Respuesta ideal']
    respuesta_candidato = respuestas['Respuesta candidato']
    if respuesta_ideal == respuesta_candidato:
        var = var_assigns(var, 100)
    elif respuesta_candidato == 0 and respuesta_ideal > 0:
        var = var_assigns(var, 0)
    else:
        respuesta_diff = abs(respuesta_ideal - respuesta_candidato)
        var = var_assigns(var, max(100 - (respuesta_diff * 15), 0))

    return var

def ponderado_candidatos(nuevos_candidatos_list : list):
    for candidato in nuevos_candidatos_list:
        try:
            preguntas_preseleccion = candidato.preguntas_preseleccion

            experiencia_cargo_ponde = None
            experiencia_herramienta_ponde = None
            nivel_ingles_ponde = None
            titulo_ponde = None
            for llave, valor in preguntas_preseleccion.items():
                respuesta_ideal = valor['Respuesta ideal']
                respuesta_candidato = valor['Respuesta candidato']
                if 'experiencia tienes como' in llave:
                    experiencia_cargo_ponde = numerical_calculator(experiencia_cargo_ponde, valor)
                elif 'experiencia tienes con' in llave:
                    experiencia_herramienta_ponde = numerical_calculator(experiencia_herramienta_ponde, valor)
                elif '¿Cuál es tu nivel de Inglés?' in llave:
                    if respuesta_ideal == respuesta_candidato:
                        nivel_ingles_ponde = 100
                    else:
                        nivel_ingles_ponde = 0
                elif 'obtenido el siguiente' in llave:
                    if respuesta_ideal == respuesta_candidato:
                        titulo_ponde = 100
                    else:
                        titulo_ponde = 0

            Ponderado.objects.create(
                experiencia_cargo = experiencia_cargo_ponde,
                experiencia_herramienta = experiencia_herramienta_ponde,
                nivel_ingles = nivel_ingles_ponde,
                titulo_academico = titulo_ponde,
                id_candidato = candidato
            )

            logging.info(f'Candidato {candidato.nombre_candidato} ponderado correctamente')

        except Exception as e:
            logging.error(f'ERROR al ponderar al Candidato {candidato.nombre_candidato}: {e}')

def explore_linkedin_ad(url_anuncio: str, username: str, password: str):
    try:
        data = linkedin_candidatos.linkedin_candidatos(url_anuncio, username, password)
    except Exception as ex:
        data = None
        logging.error(f'No se pudo ejecutar el buscador en la oferta {url_anuncio}, {ex}')
    if data:
        response = create_or_update_ofertas(data)
        if response["status"] == "success":
            if response["nuevos_candidatos_count"] > 0:
                ponderado_candidatos(response["nuevos_candidatos_list"])