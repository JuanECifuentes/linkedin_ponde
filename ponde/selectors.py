from .models import *

def get_all_ofertas():
    ofertas = OfertasLaborales.objects.all()

    data = {oferta.id: oferta for oferta in ofertas}
    return data