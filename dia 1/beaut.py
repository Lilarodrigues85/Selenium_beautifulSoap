import requests
from bs4 import BeautifulSoup

response = requests.get('https://g1.globo.com/')

content = response.content

site = BeautifulSoup(content, 'html.parser')

#html da noticia
post = site.find('div', attrs={'class':'feed-post-body'})

#titulo
titulo = post.find ('a', attrs={'class':'feed-post-link gui-color-primary gui-color-hover'} )

print(titulo.text)


