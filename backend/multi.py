
import multiprocessing
from selenium import webdriver
#Libraries
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def findAddress(driver):
    address = driver.find_element(By.CLASS_NAME,"text-left.d-flex.flex-inline")
    driver.implicitly_wait(1)
    address = address.get_attribute("outerHTML")
    soup = BeautifulSoup(address, "html.parser")
    address = soup.findAll()[1].text
    return address

def findRent():
    rent = driver.find_element(By.ID,"price-month")
    driver.implicitly_wait(1)
    rent = rent.get_attribute("outerHTML")
    soup = BeautifulSoup(rent, "html.parser")
    rent = soup.findAll()[1].text
    return rent
# Funcion para cambiar de pagina
# Parametros:
# driver: driver de selenium
# page: numero de pagina a la que se quiere ir    
def turnPage(driver,page):
    #bajar al fondo de la pagina
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #Click en siguiente pagina
    nextPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[aria-label='Go to next page']")))
    iterator = 1
    while (iterator < page and nextPage.is_enabled()):
        driver.implicitly_wait(10)
        nextPage.click()
        iterator = iterator + 1
    driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
    return True
# Funcion para calcular la cantidad de paginas
# Parametros:
# driver: driver de selenium   
def calculatePagination(driver):
    #bajar al fondo de la pagina
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #Click en siguiente pagina
    nextPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[aria-label='Go to next page']")))
    driver.implicitly_wait(10)
    counter = 1
    while (nextPage.is_enabled()):
        counter = counter + 1
        nextPage.click()
        driver.implicitly_wait(10)
    previousPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[aria-label='Go to previous page']")))        
    while (previousPage.is_enabled()):
        previousPage.click()
        driver.implicitly_wait(10)   
    return counter
def writeExcel(addresses, rents, bedrooms, parkings, gastosComunes, urlImages, pets, areas, orientations):
    columns= ['Dirección','Valor de arriendo','Dormitorios','Estacionamientos','Gastos comunes','URL 1º foto',\
        '¿Acepta mascotas?','Superficie total','Orientación']
    # Create DataFrame from multiple lists
    df = pd.DataFrame(list(zip(addresses, rents, bedrooms, parkings, gastosComunes, urlImages, pets, areas, orientations)), columns=columns)
    print(df)
    # Write DataFrame to Excel file
    df.to_excel('Output.xlsx')    
def scrape(url,index,page):
    driver = webdriver.Chrome()
    print("Index = " + str(index))
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(url)
    driver.implicitly_wait(10)
    if (page != 1):
        print("Page: " + str(page))
        turnPage(driver,page)
        driver.implicitly_wait(10)
    #driver.implicitly_wait(10)
    #elementsAux = driver.find_elements(By.CLASS_NAME,"carousel-card-a")
    elementsAux = WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"carousel-card-a")))
    driver.implicitly_wait(10)
    element = elementsAux[index]
    if (index>=4):
        driver.implicitly_wait(10)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    element.click()
    driver.implicitly_wait(10)    
    address = findAddress(driver)
    print(address)
    driver.close()
    # do something with the page source

# os.environ['PATH'] += r"C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe"
# Chrome driver executable path
os.environ['PATH'] += r"C:/home/javierlopez/Documentos/fullstack-test-tango/backend/"
driver = webdriver.Chrome()
driver.maximize_window()
url = "https://renter.tangoapp.rent/advanced-search?p=all"
driver.implicitly_wait(10)
driver.get(url)
#Lists of data
addresses = []
rents = []
bedrooms = []
parkings = []
gastosComunes = []
urlImages = []
pets = []
areas = []
orientations = []

pages = calculatePagination(driver) 
driver.implicitly_wait(10)
driver.close()
  

processes = []
i = 0
elementMaxSize = 3
while i < 3:
    processes = []
    p = multiprocessing.Process(target=scrape, args=(url,2,i))
    p.start()
    processes.append(p)
    i +=1
for p in processes:
    p.join()