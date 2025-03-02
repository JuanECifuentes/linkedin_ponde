import logging
from .bots.commands import *

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)

def explore_linkedin_ad(url_anuncio: str, username: str, password: str):
    #try:
    if True:
        data = linkedin_candidatos.linkedin_candidatos(url_anuncio, username, password)
        print(data)
    """ except Exception as ex:
        data = None
        logging.error(f'No se pudo ejecutar el buscador en la oferta {url_anuncio}, {ex}') """
    if data:
        return data