import time
import random
import pandas as pd

from time import sleep
from datetime import datetime, timedelta, date

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


BASE_URL = "https://cinemas.com.ni/cartelera/"
MOVIES = []

options = Options()
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get(BASE_URL)
driver.implicitly_wait(15)

now = datetime.now()
hoy = now.strftime("%m/%d/%Y")
# 1
class Funcion:
    titulo = ""
    fecha = ""
    sala = ""
    hora = ""

    def print_titulo(self):
        print(self.titulo)

    def print_fecha(self):
        print(self.fecha)

    def print_sala(self):
        print(self.sala)

    def print_hora(self):
        print(self.hora)


peliculas = driver.find_elements(by=By.XPATH, value="//section/div/div/div/a[@class]")

conteo = 0
titulo = ""
funciones = Funcion()

for i, p in enumerate(peliculas):
    sleep(random.uniform(2.0, 4.0))
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-red".replace(" ", ".")))
    )

    nuevo = driver.find_elements(by=By.XPATH, value="//section/div/div/div/a[@class]")
    nuevo[conteo].click()
    conteo = conteo + 1
    sleep(random.uniform(2.0, 4.0))

    # datos dentro de la pagina de funciones
    try:
        funciones.titulo = driver.find_element(
            by=By.XPATH, value="//*[@id='info-right']/div/div[1]/h2"
        ).text
        funciones.print_titulo()  ############# titulo peli
        tit = funciones.titulo
        print(tit)
        for x in range(2, 7):
            driver.find_element(by=By.XPATH, value='//*[@id="cnm_mov"]').click()
            cin = driver.find_element(
                by=By.XPATH, value='//*[@id="cnm_mov"]/option[{}]'.format(x)
            ).text
            print(cin)
            print(
                driver.find_element(
                    by=By.XPATH, value='//*[@id="cnm_mov"]/option[{}]'.format(x)
                ).text
            )  ############ cine tambien ------- guardar x
            driver.find_element(
                by=By.XPATH, value='//*[@id="cnm_mov"]/option[{}]'.format(x)
            ).click()
            sleep(random.uniform(2.0, 4.0))

            tata = driver.find_elements(
                by=By.CSS_SELECTOR,
                value="div.col-12.col-sm-4.col-md-6.col-lg-4.list-horarios.d1.show-tandas",
            )
            conteo_tata = 0
            for a in enumerate(tata):
                tata2 = driver.find_elements(
                    by=By.CSS_SELECTOR,
                    value="div.col-12.col-sm-4.col-md-6.col-lg-4.list-horarios.d1.show-tandas",
                )
                sala = tata2[conteo_tata].find_element(by=By.XPATH, value="./h4")
                if sala.text == "":
                    print("no tiene horario")
                    continue
                horas = tata2[conteo_tata].find_elements(by=By.XPATH, value="./div/a")
                sal = sala.text
                print(sal)
                print(sala.text)  ############## sala
                conteo_hora = 0
                for h in enumerate(horas):
                    #### pobtencion de las asistencias
                    #######guardar conteo_tata
                    horas2 = tata2[conteo_tata].find_elements(
                        by=By.XPATH, value="./div/a"
                    )
                    hor = horas2[conteo_hora].text
                    print(hor)
                    print(horas2[conteo_hora].text)  ########### hora
                    url = driver.current_url  ############ url
                    print(url)
                    data = {
                        "Theatre Name": cin,
                        "Country": "NI",
                        "title": tit,
                    }
                    MOVIES.append(data)
                    conteo_hora = conteo_hora + 1
                    # insetar a la base
                conteo_tata = conteo_tata + 1
        driver.back()

    except Exception:
        print("La pelicula no tiene horarios")
        driver.back()

df = pd.DataFrame(MOVIES)
df.to_csv(f"Cinemas_{date.today()}.csv", index=False)
print(f"Datos guardados en el archivo Cinemas_{date.today()}.csv")
driver.quit()
