from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import json

#tratar a versão do driver
servico = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=servico)

url = 'https://elivros.love/LivrosGratis'

driver.get(url)

dados_coletados = []

usa_scroll_infinito = False

def extrair_dados():
  page_content = driver.page_source
  soup = BeautifulSoup(page_content, 'html.parser')

  dados = soup.find_all('div', class_='onText')
  for dado in dados:
    item_texto = dado.get_text(strip=True)
    dados_coletados.append({"conteudo": item_texto})

def salvar_dados ():
  with open ('dados.json', 'w', encoding='utf-8') as f:
    json.dump(dados_coletados, f, ensure_ascii=False, indent=4 )
  print("Dados salvos em dados.json")

try:
  if usa_scroll_infinito:
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
      extrair_dados()
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(2)

      new_height = driver.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
        print("Fim do conteúdo para carregamento.")
        break
      last_height = new_height
  else:

    while True:
      extrair_dados()
      try:

        next_button = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, '//*[@id="PaginationMain"]/ul[1]/li/a')))
        
        next_button.click()
        time.sleep(2)
      except:
        print("Fim da paginação ou botão 'Próxima' não encontrado")

finally:

  salvar_dados()

  driver.quit()