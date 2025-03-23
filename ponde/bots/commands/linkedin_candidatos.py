import time
import logging
import pandas as pd
from datetime import datetime
from django.conf import settings
from playwright.sync_api import sync_playwright

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)

def linkedin_candidatos(url_anuncio: str, username: str, password: str):
    logging.info(f'Inicio Scrapping {url_anuncio}')

    year = datetime.now().year

    with sync_playwright() as p:

        browser_path = settings.BROWSER_PATH

        navegador = p.chromium

        if browser_path:
            browser = navegador.launch(
                headless=False, args=['--disable-blink-features=AutomationControlled'],
                executable_path=browser_path,
            )
        else:
            browser = navegador.launch(headless=False, args=['--disable-blink-features=AutomationControlled'])
        

        context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
            )


        page = context.new_page()

        page.evaluate("""

                Object.defineProperty(navigator, 'webdriver', {

                    get: () => undefined

                });

            """)

        page.goto(url_anuncio)

        final_data = {
            "anuncio": {},
            "caught": 0,
            "issues": 0,
            "exceptions": [],
            "conection_issues": 0,
            "process_data": {}
        }
        
        logging.info(f"Getting url: {url_anuncio}")
        time.sleep(3)

        final_data['anuncio']['url'] = url_anuncio

        username_input = page.query_selector('#username')
        if username_input:
            username_input.fill(username)
        else:
            logging.error('No se encontro el campo de usuario')

        password_input = page.query_selector('#password')
        if password_input:
            password_input.fill(password)
        else:
            logging.error('No se encontro el campo de contraseña')

        forgot_checkbox = page.query_selector('//*[@id="rememberMeOptIn-checkbox"]')
        if forgot_checkbox:
            page.evaluate('''
                        document.getElementById("rememberMeOptIn-checkbox").checked = false;
                        document.getElementById("rememberMeOptIn-checkbox").value = false;
                        ''')
        else:
            logging.error('No se encontro el checkbox de recordar contraseña')

        login_button = page.query_selector('button[type="submit"]')
        if login_button:
            login_button.click()
        else:
            logging.error('No se encontro el boton de login')

        time.sleep(5)

        try:
            cargo = page.query_selector('div.artdeco-entity-lockup__title.ember-view.display-flex.align-items-center p').text_content()
            final_data['anuncio']['cargo'] = cargo.replace('\n', '').replace('  ','').replace('Cargo','').strip()
        except Exception as e:
            logging.error('No se encontro el titulo del cargo')
            final_data['exceptions'].append(e)

        candidatos = page.query_selector_all('ul.artdeco-list li a')

        for index, candidato in enumerate(candidatos):
            row_dict = {}
            candidato.click()
            time.sleep(2)
            link = f'https://www.linkedin.com{candidato.get_attribute("href")}'

            nombre_candidato = page.query_selector('//*[@id="hiring-detail-root"]/div[1]/div[1]/div[1]/h1')
            ubicacion = page.query_selector('//*[@id="hiring-detail-root"]/div[1]/div[1]/div[1]/div[1]/div[2]')

            try:
                enlace = page.query_selector('div.artdeco-card.mt4.p0 div.hiring-profile-highlights__see-full-profile a').get_attribute('href')
            except:
                enlace = None


            row_dict['Link'] = link
            row_dict['Nombre'] = nombre_candidato.text_content().replace('Solicitud','').strip() if nombre_candidato else str(index)
            row_dict['Ubicacion'] = ubicacion.text_content().strip() if ubicacion else ''
            row_dict['Enlace perfil'] = f'https://www.linkedin.com{enlace}' if enlace else None
            row_dict['Experiencia'] = {}
            row_dict['Educacion'] = {}
            row_dict['Curriculum'] = None
            row_dict['Preseleccion'] = {}

            experiece_card = page.query_selector_all('//*[@id="hiring-detail-root"]/div[2]/div[1]/section[1]/ul/li')
            for exp in experiece_card:
                try:
                    exp_title = exp.query_selector('xpath=//div//p[1]').text_content().strip()
                    exp_site = exp.query_selector('xpath=//div//p[2]').text_content().strip()
                    try:
                        exp_time = exp.query_selector('xpath=//div//p[3]//span[2]').text_content().replace('actualidad',str(year)).strip()
                    except:
                        exp_time = 'No especificado'
                    if exp_title not in row_dict['Experiencia']:
                        row_dict['Experiencia'][exp_title] = {'Empresa': exp_site, 'Tiempo': exp_time}
                    else:
                        row_dict['Experiencia'][f'{exp_title} - {exp_site}'] = {'Empresa': exp_site, 'Tiempo': exp_time}
                except Exception as ex:
                    logging.error(f'Error al obtener la experiencia del candidato {ex}')

            education_card = page.query_selector_all('//*[@id="hiring-detail-root"]/div[2]/div[1]/section[2]/ul/li')
            for edu in education_card:
                try:
                    edu_title = edu.query_selector('xpath=//div//p[1]').text_content().strip()
                    edu_site = edu.query_selector('xpath=//div//p[2]').text_content().strip()
                    try:
                        edu_time = edu.query_selector('xpath=//div//p[3]//span[2]').text_content().replace('actualidad',str(year)).strip()
                    except:
                        edu_time = 'No especificado'

                    if edu_title not in row_dict['Educacion']:
                        row_dict['Educacion'][edu_title] = {'Titulo': edu_site, 'Tiempo': edu_time}
                    else:
                        row_dict['Educacion'][f'{edu_title} - {edu_site}'] = {'Titulo': edu_site, 'Tiempo': edu_time}
                except Exception as ex:
                    logging.error(f'Error al obtener la educacion del candidato {ex}')

            try:
                curriculum_a = page.query_selector_all('div.p0.mt4.artdeco-card a') #TODO No esta trayendo bien el curriculum
                for cur in curriculum_a:
                    href = cur.get_attribute('href')
                    if 'www.linkedin.com' in href:
                        row_dict['Curriculum'] = href
                        break
            except:
                logging.error('No se encontro el curriculum del candidato')

            preseleccion_li = page.query_selector_all('div.hiring-screening-questions.artdeco-card ul li')
            for preg in preseleccion_li:
                try:
                    preg_title = preg.query_selector('xpath=//div//p[1]').text_content().strip()
                    preg_resp_ideal = preg.query_selector('xpath=//div//p[2]//span[2]').text_content().strip().upper().replace('YES','SI').replace('SÍ','SI')
                    try:
                        preg_resp_ideal = int(preg_resp_ideal)
                    except:
                        pass
                    preg_resp_candidato = preg.query_selector('xpath=//div//p[3]').text_content().replace('Respuesta del candidato\n','').strip().upper().replace('YES','SI').replace('SÍ','SI')
                    try:
                        preg_resp_candidato = int(preg_resp_candidato)
                    except:
                        pass
                    row_dict['Preseleccion'][preg_title] = {'Respuesta ideal': preg_resp_ideal, 'Respuesta candidato': preg_resp_candidato}
                except Exception as ex:
                    logging.error(f'Error al obtener la pregunta de preseleccion del candidato {ex}')

            final_data['process_data'][row_dict['Nombre']] = row_dict
            final_data['caught'] += 1
            logging.info(f"{row_dict['Nombre']} was processed successfully") #TODO Falta comprobar que tome todas las ofertas

            if index == 20:
                break

    return final_data





            

        
    