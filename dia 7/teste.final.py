import logging
import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Configuração do logging
logging.basicConfig(
    filename='elivros_scraping.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configurações do Selenium com webdriver_manager
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executa o navegador em modo headless (sem interface gráfica)

# Função para extrair detalhes de cada livro
def get_book_details(book_url, driver):
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        
        driver.get(book_url)

        # Espera para garantir que o conteúdo dinâmico seja carregado
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extraindo informações principais
        title = soup.find('strong').text.strip() if soup.find('strong') else "N/A"
        author = soup.find('a', title=True)
        author_name = author.text.strip() if author else "N/A"
        
        logging.info(f"Detalhes do livro extraídos com sucesso: {title}")
        return {
            "title": title,
            "author": author_name,
            "url": book_url
        }
    except Exception as e:
        logging.error(f"Erro ao processar a página {book_url}: {e}")
    return None

# Função para rolar até o final da página
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Aumentar este tempo, se necessário
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Função principal para acessar a lista de livros
def scrape_elivros(base_url):
    book_data = []

    # Inicializa o driver do Selenium usando o ChromeDriverManager
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        logging.info(f"Acessando a página principal: {base_url}")
        driver.get(base_url)

        # Rola até o final da página para garantir que todos os livros sejam carregados
        scroll_to_bottom(driver)

        # Espera pela presença de elementos principais da lista
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a')))

        # Selecionando links para cada livro
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        book_links = soup.select('a')

        logging.info("Iniciando a extração dos livros do eLivros")
        for i, link in enumerate(book_links):# Itera sobre cada livro
            if i >= 10:
                break

            book_url = link['href']
            logging.info(f"Extraindo dados do livro {i + 1} - {book_url}")

            # Coleta dos detalhes do livro
            details = get_book_details(book_url, driver)
            if details:
                book_data.append(details)

            # Espera aleatória para simular comportamento humano
            time.sleep(random.uniform(1, 3))

    except Exception as e:
        logging.error(f"Erro ao acessar a página principal {base_url}: {e}")

    driver.quit()
    return book_data

# Função para salvar dados em JSON
def save_to_json(data, filename="elivros_livros.json"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logging.info(f"Dados salvos com sucesso em {filename}")
    except Exception as e:
        logging.error(f"Erro ao salvar dados em JSON: {e}")



# Executando o script
if __name__ == "__main__":
    base_url = "https://elivros.love/LivrosGratis"
    logging.info("Iniciando o scraping do eLivros")
    books = scrape_elivros(base_url)
    save_to_json(books)
    logging.info("Scraping concluído com sucesso")
