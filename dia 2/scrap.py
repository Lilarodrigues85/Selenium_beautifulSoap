import requests
from bs4 import BeautifulSoup
import pandas as pd

#URL da página estática
url = 'https://website-cafeteria-two.vercel.app/'

response = requests.get(url)

if response.status_code == 200:
  html_content = response.content

  soup = BeautifulSoup(html_content, 'html.parser')

  titulos = [h1.text for h1 in soup.find_all('h1')]

  links = [link.get('href') for link in soup.find_all('a')]

  imagens = [img.get('src') for img in soup.find_all('img')]

  max_len = max(len(titulos), len(links), len(imagens))

  titulos += [''] * (max_len - len(titulos))
  links += [''] * (max_len - len(links))
  imagens += [''] * (max_len - len(imagens))

  dados = {
    'Titulos': titulos,
    'Links': links,
    'Imagens': imagens
  }

  df = pd.DataFrame(dados)

  df.to_csv('dados extracao.csv', index=False)

  print("Dados salvos no arquivo 'dados extracao.csv' com sucesso!")

else:
  print(f"Erro ao acessar a página: {response.status_code}")