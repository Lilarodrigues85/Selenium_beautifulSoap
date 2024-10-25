from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

try:

  driver.get('https://www.google.com.br/')

  wait = WebDriverWait(driver, 10)

  search_box = wait.until(EC.element_to_be_clickable((By.NAME, 'q')))

  search_box.send_keys("Selenium Python")
  search_box.send_keys(Keys.RETURN)

  results = wait.until(EC.element_to_be_clickable((By.ID, "search")))

  time.sleep(5)

  print("Título da página:", driver.title)

finally:

  driver.quit()
