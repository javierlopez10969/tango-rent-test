
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
    address = WebDriverWait(driver, 700).until(EC.presence_of_element_located((By.CLASS_NAME,"text-left.d-flex.flex-inline")))
    address = address.get_attribute("outerHTML")
    soup = BeautifulSoup(address, "html.parser")
    address = soup.findAll()[1].text
    return address

def findRent(driver):
    rent = WebDriverWait(driver, 700).until(EC.presence_of_element_located((By.ID,"price-month")))
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
    nextPage = WebDriverWait(driver, 700).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[aria-label='Go to next page']")))
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
    return counter
def writeExcel(addresses, rents, bedrooms, parkings, gastosComunes, urlImages, pets, areas, orientations,nameOutputFile):
    columns= ['Dirección','Valor de arriendo','Dormitorios','Estacionamientos','Gastos comunes','URL 1º foto',\
        '¿Acepta mascotas?','Superficie total','Orientación',]
    # Create DataFrame from multiple lists
    df = pd.DataFrame(list(zip(addresses, rents, bedrooms, parkings, gastosComunes, urlImages, pets, areas, orientations)), columns=columns)
    print(df)
    # Write DataFrame to Excel file
    df.to_excel(nameOutputFile, index=False)   
def combineExcel(nameOutputFile,maxProcesses,pagination):
    writer = pd.ExcelWriter(nameOutputFile, engine='xlsxwriter')
    for i in range(1,pages+1,pagination):
        print("Procesando desde la página " + str(i) + " hasta la página " + str(i+pagination-1))
        name = "output"+str(i)+".xlsx"
        df = pd.read_excel(name)
        df.to_excel(writer, sheet_name='Sheet'+str(i), index=False)
        os.remove(name)
 
    writer.save() 

def scrape(url,pageMin,pageMax,maximumPages):
    index = 0     
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(url)
    driver.implicitly_wait(10)
    #First page
    if (pageMin != 1):
        turnPage(driver,pageMin)
        driver.implicitly_wait(10)
    wait = 900
    elementsAux = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"carousel-card-a")))
    n = len(elementsAux)
    addresses = []
    rents = []
    bedrooms = []
    parkings = []
    gastosComunes = []
    urlImages = []
    pets = []
    areas = []
    orientations = []
    pages = []
    indexes = []
    page = pageMin
    while index != n and page <= pageMax and page <= maximumPages:        
        if (page != 1 and index != 0):
            turnPage(driver,page)
            driver.implicitly_wait(10) 
        if (index>=3):
            driver.implicitly_wait(10)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(10)
        elementsAux = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"carousel-card-a")))
        e = elementsAux[index]
        try:
            e.click()
        except:
            break
        address = findAddress(driver)
        rent = findRent(driver)
        
        #Dormitorios
        info= WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.CLASS_NAME,"info")))
        elements = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"img-detail")))
        bedroom = elements[0].text

        #Estacionamientos
        parking = elements[4].text

        #Superficie total/
        areasAux =info.find_elements(By.XPATH,"//*[contains(text(), 'm²')]")
        a1 = int(areasAux[0].text.split(" ")[0])
        a2 = int(areasAux[1].text.split(" ")[0])
        totalArea = a1 + a2

        #Gastos comunes
        elements = driver.find_elements(By.TAG_NAME,"span")
        driver.implicitly_wait(1)
        gastoComun = elements[5].text

        #¿Acepta mascotas?
        pet = elements[7].text

        #URL 1º foto
        imageContainer= driver.find_element(By.CLASS_NAME,"images")
        images = imageContainer.find_elements(By.TAG_NAME,"img")
        driver.implicitly_wait(1)
        urlImage = images[0].get_attribute("src")

        #Orientación
        #Find detalle propiedad
        element = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.CLASS_NAME,"MuiPaper-root.MuiAccordion-root.MuiAccordion-rounded.MuiPaper-elevation1.MuiPaper-rounded")))
        element.click()
        time.sleep(0.3)

        #Find orientacion
        orientacion = element.find_elements(By.XPATH,"//*[contains(text(), 'Orientación')]") 
        orientacion = orientacion[0].text

        #Guardar en listas
        addresses.append(address)
        rents.append(rent)
        bedrooms.append(bedroom)
        parkings.append(parking)
        gastosComunes.append(gastoComun)
        urlImages.append(urlImage)
        pets.append(pet)
        areas.append(totalArea)
        orientations.append(orientacion)
        pages.append(page)
        indexes.append(index)

        output = "Indexඞ"+ str(index) + "ඞPageඞ" + str(page) + "ඞAddressඞ"+address + "ඞRentඞ" + rent + "ඞDormitoriosඞ"+bedroom
        output += "ඞEstacionamientosඞ" + parking + "ඞGastos comunesඞ" + gastoComun + "ඞURL 1º fotoඞ" + urlImage + "ඞ¿Acepta mascotas?ඞ" + pet 
        output += "ඞSuperficie totalඞ" + str(totalArea) + "ඞOrientaciónඞ" + orientacion
        #split by ඞ
        print(output.split("ඞ"))
        index += 1
        driver.back()
        if (index == n):
            index = 0
            page += 1
            turnPage(driver,page)
            driver.implicitly_wait(10)
            elementsAux = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"carousel-card-a")))
            n = len(elementsAux)    
    driver.close()
    nameOutput = "output" + str(pageMin) + ".xlsx"
    writeExcel(addresses, rents, bedrooms, parkings, gastosComunes, urlImages, pets, areas, orientations, nameOutput)

    return True
    # do something with the page source
start = time.time()
# os.environ['PATH'] += r"C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe"
# Chrome driver executable path
os.environ['PATH'] += r"C:/home/javierlopez/Documentos/fullstack-test-tango/backend/"
driver = webdriver.Chrome()
driver.maximize_window()
url = "https://renter.tangoapp.rent/advanced-search?p=all"
driver.implicitly_wait(10)
driver.get(url)

driver.implicitly_wait(10)
pages = calculatePagination(driver) 
driver.close()

processes = []
i = 1
maxProcesses = 3

if(pages % maxProcesses == 0):
    pagination = pages// maxProcesses
else:
    pagination = pages//maxProcesses + pages%maxProcesses

for i in range(1,pages+1,pagination):
    print("Procesando desde la página " + str(i) + " hasta la página " + str(i+pagination-1))
    p = multiprocessing.Process(target=scrape, args=(url,i,i+pagination-1,pages))
    p.start()
    processes.append(p)
for p in processes:
    p.join()

combineExcel("output.xlsx",maxProcesses,pagination)
end = time.time()
diff = end - start
print("Tiempo de ejecución : " + str(diff) + " segundos")