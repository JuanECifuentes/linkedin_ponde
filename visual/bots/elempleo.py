import time
import logging
import pandas as pd
from django.conf import settings
from ..utils import crear_ofertas
from playwright.sync_api import sync_playwright

def elempleo(cargo,cantidad_ofertas: int = None):
    url = 'https://www.elempleo.com/'

    with sync_playwright() as p:

        browser_path = settings.BROWSER_PATH

        navegador = p.chromium

        if browser_path:
            browser = navegador.launch(
                headless=True, args=['--disable-blink-features=AutomationControlled'],
                executable_path=browser_path
            )
        else:
            browser = navegador.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])

        context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
            )


        page = context.new_page()

        page.evaluate("""

                Object.defineProperty(navigator, 'webdriver', {

                    get: () => undefined

                });

            """)

        page.goto(url)
        page.wait_for_selector('.box.empleo')

        page.click('.box.empleo')
        time.sleep(3)

        page.fill('#searchBox',cargo)
        page.click('.searchbox-wrapper button.btn.btn-primary.js-btn-search')
        time.sleep(3)

        lista_ofertas = page.query_selector_all('.result-item')

        if cantidad_ofertas:
            lista_ofertas = lista_ofertas[:cantidad_ofertas]

        url_ofertas = []

        for oferta in lista_ofertas:
            href = oferta.query_selector('a.text-ellipsis.js-offer-title').get_attribute('href')
            url_ofertas.append(f'https://www.elempleo.com/{href}')

        data = []

        for url_oferta in url_ofertas:
            page.goto(url_oferta)
            time.sleep(3)

            titulo = page.query_selector('h1.ee-mod.ee-offer-title.js-offer-title').text_content().replace('\n','').replace('   ','').strip()

            try:
                salario = page.query_selector('div.col-xs-12.col-md-8.offer-data div.col-xs-12.col-sm-6.data-column p:has(i.fa-money)').text_content().replace('COP','').replace('\n','').replace('   ','').strip()
            except:
                salario = 'No Mencionado'

            try:
                ubi = page.query_selector('div.col-xs-12.col-md-8.offer-data div.col-xs-12.col-sm-6.data-column p:has(i.fa-map)').text_content().replace('\n','').replace('   ','').strip()
            except:
                ubi = 'No Mencionado'

            data.append({ titulo : {
                'titulo_oferta' : titulo,
                'salario' : salario,
                'ubicacion' : ubi
            }})
    return data

def elempleo_source(cargo = 'montacarguista',cantidad_ofertas = None, page = 'ELEMPLEO'):
    try:
        data = elempleo(cargo,cantidad_ofertas)
        print(data)
    except:
        data = None
        logging.error(f'No se pudo ejecutar el buscador {page}')
    
    if data:
        crear_ofertas(data,page)