from .models import Ofertas

def crear_ofertas(data,page):
    # Iterar sobre el contenido de data
    for item in data:
        for titulo, detalles in item.items():
            # Extraer los datos
            titulo_oferta = detalles['titulo_oferta']
            salario = detalles['salario']
            ubicacion = detalles['ubicacion']
            
            # Crear y guardar la oferta en la base de datos
            oferta = Ofertas.objects.create(
                titulo_oferta=titulo_oferta,
                salario=salario,
                ubicacion=ubicacion,
                page=page
            )
            oferta.save()