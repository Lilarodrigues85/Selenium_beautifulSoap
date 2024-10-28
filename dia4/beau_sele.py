from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep

options = Options()
options.add_argument('--headless')


#configurando o Selenium e abrindo o navegador
driver = webdriver.Chrome() # ou webdriver.Firefox() conforme o navegador

driver.get('https://www.airbnb.com')

wait = WebDriverWait(driver, 15)


# search_box = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'input')))
# search_box.send_keys("São Paulo")
# search_box.send_keys(Keys.RETURN)



input_place = driver.find_element(By.TAG_NAME, 'input')
input_place.send_keys('São Paulo')
input_place.submit()




# site = BeautifulSoup(driver.page_source, 'html.parser')

# with open('saida.html', 'w', encoding='utf-8') as f:
    # f.write(site.prettify())
