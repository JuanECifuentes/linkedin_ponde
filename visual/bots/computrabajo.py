import time
import logging
import pandas as pd
from django.conf import settings
from ..utils import crear_ofertas
from playwright.sync_api import sync_playwright

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)

def computrabajo(cargo = 'montacarguista',cantidad_ofertas = None):
    logging.info('Inicio Scrapping computrabajo')
    url = 'https://co.computrabajo.com/'

    with sync_playwright() as p:

        browser_path = settings.BROWSER_PATH

        navegador = p.chromium

        proxy_server = "wss://brd-customer-hl_cf834278-zone-scraping_browser3:o33cc0ijm8fz@brd.superproxy.io:9222"

        """if browser_path:
            browser = navegador.launch(
                headless=True, args=['--disable-blink-features=AutomationControlled'],
                executable_path=browser_path, proxy={"server": proxy_server}
            )
        else:
            browser = navegador.launch(headless=True, args=['--disable-blink-features=AutomationControlled'],proxy={"server": proxy_server})"""
        
        browser = navegador.connect_over_cdp(proxy_server)

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
        logging.info(f"Getting url: {url}")
        page.wait_for_selector('#prof-cat-search-input')

        page.fill('#prof-cat-search-input',cargo)

        page.click('#search-button')
        time.sleep(3)

        page.evaluate('''() => {
                      console.log("se ejecuto")
            const element = document.querySelector("#pop-up-webpush-sub > div:nth-child(2) > div > button:nth-child(1)");
            if (element) {
            element.click();
            }
        }''')

        lista_ofertas = page.query_selector_all('#offersGridOfferContainer .box_offer')

        if cantidad_ofertas:
            lista_ofertas = lista_ofertas[:cantidad_ofertas]

        data = []

        for oferta in lista_ofertas:
            logging.info(f"Getting Oferta")
            oferta.click()
            time.sleep(2)
            try:
                data_id = oferta.get_attribute('data-id')
            except:
                data_id = None

            titulo = page.query_selector(f'div.box_detail[data-id="{data_id}"] p' if data_id else '/html/body/main/div[8]/div/div[2]/div[2]/p').text_content().replace('\n','').replace(' ','').strip()

            try:
                salario = page.query_selector('div.fs14.mb10 p:has(span.i_money)').text_content().replace('\n','').strip()
            except:
                salario = 'No Mencionado'

            try:
                ubi = page.query_selector('div.header_detail p.fs16.mb5').text_content().replace('\n','').strip()
            except:
                ubi = 'No Mencionado'

            #(titulo,salario,ubi)
            data.append({ titulo : {
                'titulo_oferta' : titulo,
                'salario' : salario,
                'ubicacion' : ubi
            }})
    return data

def computrabajo_source(cargo = 'montacarguista',cantidad_ofertas = None, page = 'COMPUTRABAJO'):
    try:
        data = computrabajo(cargo,cantidad_ofertas)
        print(data)
    except Exception as ex:
        data = None
        logging.error(f'No se pudo ejecutar el buscador {page}, {ex}')
    if data:
        crear_ofertas(data,page)
        return data