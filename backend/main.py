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
def turnPage(driver,page):
    #bajar al fondo de la pagina
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    nextPage = driver.find_element(By.CSS_SELECTOR,"[aria-label='Go to next page']")
    iterator = 1
    while (iterator < page):
        driver.implicitly_wait(10)
        nextPage.click()
        iterator = iterator + 1
    driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
def writeExcel(addresses, rents, bedrooms, parkings, gastosComunes, urlImages, pets, areas, orientations):
    columns= ['Dirección','Valor de arriendo','Dormitorios','Estacionamientos','Gastos comunes','URL 1º foto',\
        '¿Acepta mascotas?','Superficie total','Orientación']
    # Create DataFrame from multiple lists
    df = pd.DataFrame(list(zip(addresses, rents, bedrooms, parkings, gastosComunes, urlImages, pets, areas, orientations)), columns=columns)
    print(df)
    # Write DataFrame to Excel file
    df.to_excel('Output.xlsx')    

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


driver.implicitly_wait(10)
elementsAux = driver.find_elements(By.CLASS_NAME,"carousel-card-a")

index = 0
page = 1
while (index < len(elementsAux)):
    driver.implicitly_wait(10)
    elementsAux = driver.find_elements(By.CLASS_NAME,"carousel-card-a")
    # Si la pagina es distinto de 1
    if (page != 1):
        print("Page: " + str(page))
        turnPage(driver,page)
    if (index>4):
        driver.implicitly_wait(10)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Index: " + str(index))
    print("Page: " + str(page))
    print("Elements: " + str(len(elementsAux)))
    e = elementsAux[index]
    driver.implicitly_wait(10)
    try:
        e.click()
    except:
        break
    #Direccion
    
    address = findAddress(driver)
    print(address)
    addresses.append(address)

    #Valor de arriendo
    rent = findRent()
    print(rent)
    rents.append(rent)

    #Dormitorios
    info = driver.find_element(By.CLASS_NAME,"info")
    driver.implicitly_wait(1)
    elements = info.find_elements(By.CLASS_NAME,"img-detail")

    bedroom = elements[0].text
    print(bedroom)
    bedrooms.append(bedroom)

    #Estacionamientos
    parking = elements[4].text
    print(parking)
    parkings.append(parking)

    #Superficie total/
    areasAux =info.find_elements(By.XPATH,"//*[contains(text(), 'm²')]")
    a1 = int(areasAux[0].text.split(" ")[0])
    a2 = int(areasAux[1].text.split(" ")[0])
    totalArea = a1 + a2
    area = str(totalArea) + " m2"
    print(area) 
    areas.append(area)

    #Gastos comunes
    elements = driver.find_elements(By.TAG_NAME,"span")
    driver.implicitly_wait(1)
    gastoComun = elements[5].text
    print("Gastos comunes: " + gastoComun)
    gastosComunes.append(gastoComun)

    #¿Acepta mascotas?
    pet = elements[7].text
    print("¿Acepta mascotas? " + pet)
    pets.append(pet)

    #URL 1º foto
    imageContainer= driver.find_element(By.CLASS_NAME,"images")
    images = imageContainer.find_elements(By.TAG_NAME,"img")
    driver.implicitly_wait(1)
    urlImage = images[0].get_attribute("src")
    print(urlImage)
    urlImages.append(urlImage)

    #Orientación
    #Find detalle propiedad
    element = driver.find_element(By.CLASS_NAME,"MuiPaper-root.MuiAccordion-root.MuiAccordion-rounded.MuiPaper-elevation1.MuiPaper-rounded")
    driver.implicitly_wait(4)
    element.click()
    time.sleep(0.3)
    #Find orientacion
    orientacion = element.find_elements(By.XPATH,"//*[contains(text(), 'Orientación')]") 
    orientacion = orientacion[0].text
    print("Orientación: " + orientacion)
    orientations.append(orientacion)
    index +=1
    driver.back()
    if (index == len(elementsAux)):
        index = 0
        page +=1


driver.close()

writeExcel(addresses, rents, bedrooms, parkings, gastosComunes, urlImages, pets, areas, orientations )
