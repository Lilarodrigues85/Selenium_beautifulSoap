from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time

# Inicializa o driver do Selenium (certifique-se de que o ChromeDriver está instalado e no PATH)
driver = webdriver.Chrome()

# Acesse a página inicial do site
driver.get("https://elivros.love/")
time.sleep(2)  # Aguarda o carregamento da página

# Lista para armazenar os dados extraídos
dados_extraidos = []

# Loop para navegar pelas páginas de resultados
while True:
    # Obtém o HTML da página atual
    page_source = driver.page_source

    # Analisa o HTML com BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Encontra os itens desejados (livros)
    items = soup.find_all('div', class_='post')  # Altere conforme a estrutura do site

    # Extrai as informações de cada item encontrado
    for item in items:
        titulo_tag = item.find('strong')  # O título geralmente está em um <h2>
        autor_tag = item.find('a', class_='author')  # Altere para a classe correta do autor

        # Extrai o texto ou define um valor padrão caso o item não seja encontrado
        titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Título não encontrado"
        autor = autor_tag.get_text(strip=True) if autor_tag else "Autor não encontrado"
        
        # Adiciona os dados em um dicionário
        dados_extraidos.append({
            "titulo": titulo,
            "autor": autor
        })

    # Tenta localizar o botão "Próxima página" para navegar
    try:
        next_button = driver.find_element(By.LINK_TEXT, "Próxima")  # Altere conforme necessário
        next_button.click()
        time.sleep(2)  # Espera o carregamento da próxima página
    except:
        print("Fim da paginação ou botão 'Próxima' não encontrado.")
        break

# Fecha o driver do Selenium
driver.quit()

# Salva os dados em um arquivo JSON
with open("dados_elivros.json", "w", encoding="utf-8") as f:
    json.dump(dados_extraidos, f, ensure_ascii=False, indent=4)

print("Dados salvos em 'dados_elivros.json'")