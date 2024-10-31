import logging
import json
import csv
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

#logging
logging.basicConfig(
  filename='imdb_scraping;log', #log
  level=logging.INFO,           #logging
  format='%(asctime)s - %(levelname)s - %(message)s',
  datefmt='%y-%m-%d %H:%M:%S'
)

#selenium com webdriver_manager
options = webdriver.ChromeOptions()
#options.add_argument("--headless")

#coleta de dados dos filmes
def get_movie_details(movie_url, driver):
  
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=options))
  
  try:

    driver.get(movie_url)

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "h1")))

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ratingValue')))

    #links de cada filme
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #informações principais
    title = soup.find('h1').text.strip() if soup.find('h1') else "N/A"
    rating = soup.find(class_='ratingValue').strong.span.text.strip() if soup.find(class_='ratingValue') else "N/A"
    year = soup.find(id="titleYear").a.text.strip() if soup.find(id="titleYear") else "N/A"
    genres = [g.text.strip() for g in soup.find_all(class_='genre')] if soup.find_all(class_='genre') else "N/A"

    logging.info(f"Detalhes do filme extraídos com sucesso: {title}")
    return {
      "title": title,
      "rating": rating,
      "year": year,
      "genres": genres
    }
  
  except Exception as e:
    logging.error(f"Erro a processar a página {movie_url}: {e}")
  return None

#scroll
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Rola para baixo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Espera um pouco para a nova parte da página ser carregada
        time.sleep(2)  
        
        # Calcula a nova altura da página
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Se a altura não mudou, chegamos ao final
        if new_height == last_height:
            break
        last_height = new_height

#acessar lista de filmes
def scrape_imdb_top_movies(base_url):
  movie_data = []

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=options))

  try:
    driver.get(base_url)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td.titleColumn a')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    movie_links = soup.select('td.titleColumn a')

    logging.info("Iniciando aa extração dos filmes do IMDb Top 250")
    for i, link in enumerate(movie_links[:250]):
      movie_url = "https://www.imdb.com" + link['href']
      logging.info(f"Estraindo dados do filme {i+1} - {movie_url}")

      #detalhes dos filmes
      details = get_movie_details(movie_url, driver)
      if details:
        movie_data.append(details)
      
      #Espera aleatória para simular comportamento humano
      time.sleep(random.uniform(1, 3))

  except Exception as e:
    logging.error(f"Erro ao acessar a página principal {base_url}: {e}")

  driver.quit()
  return movie_data

def save_to_json(data, filename='imdb_top_movies_json'):
  try:
    with open (filename, "w", encoding="utf-8") as file:
      json.dump(data, file, ensure_ascii=False, indent=4)
    logging.info(f"Dados salvos com sucesso em {filename}")
  except Exception as e:
    logging.error(f"Erro ao salvar dados em JSON: {e}")

#executando
if __name__ == "__main__":
  base_url = "https://www.imdb.com/chart/top/"
  logging.info("Iniciando o scraping do IMDB Top 250")
  top_movies = scrape_imdb_top_movies(base_url)
  save_to_json(top_movies)
  logging.info("Scraping concluído com sucesso")