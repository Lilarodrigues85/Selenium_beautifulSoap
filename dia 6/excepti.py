import logging
import json
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager #Gerenciador de driver
from selenium.common.exceptions import NoSuchAttributeException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from selenium.webdriver.chrome.options import Options #Importando Options

chrome_options = webdriver.ChromeOptions()

#Configuração básica de logging
logging.basicConfig(filename='scraping.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def salvar_dados(dados):
  print("Dados salvos:", dados)

def realizar_scraping(url):
  driver = None
  
  dados = []  
  try:
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    dados = {"exemplo": "dados coletados"}
    #configurando o Webdriver em modo headless

    salvar_dados(dados)

    chrome_options = Options

    #Ativando o headless
    chrome_options.add_argument("--headless")
    
    # chrome_options.add_argument("--no-sandbox")  # Opcional: para ambientes Linux
    # chrome_options.add_argument("--disable-dev-shm-usage")  # Opcional: para ambientes Docker

    #espera
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'item')))

    #BeautifulSoup fazendo parsing
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #encontrando o elemento
    livros = soup.find_all('div', class_='item')

    for livro in livros:
        titulo = livro.find('h3')  # Título do livro
        link = livro.find('a')['href'] if livro.find('a') else None  # Link do livro

        if titulo and link:
            dados.append({"titulo": titulo.text.strip(), "link": link})
            logging.info(f"Livro encontrado: {titulo.text.strip()} - {link}")
        else:
            logging.error("Título ou link do livro não encontrado.")

    
  except NoSuchAttributeException:
    logging.error("Elemento não encontrado.")
  except TimeoutException:
    logging.error("Timeout ao buscar o elemento.")
  except Exception as e:
    logging.error(f"Erro inesperado: {e}")
  

    #salvar dados em JSON e CSV
    salvar_dados(dados)
  
  def salvar_dados(dados):
    #salvando em JSON
    with open('dados.json', 'w') as json_file:
      json.dump(dados, json_file, indent=4)
    logging.info("Dados salvos em livros.json")

    #salvando em CSV
    with open('livros.csv', 'w', newline='', encoding='utf-8') as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames=["titulo", "link"])
      writer.writeheader()
      writer.writerows(dados)
    logging.info("Dados salvos em livros.csv")

if __name__ == "__main__":
  url = "https://elivros.love/LivrosGratis"
  logging.info(f"Iniciando scraping para a URL: {url}")
  salvar_dados(url)