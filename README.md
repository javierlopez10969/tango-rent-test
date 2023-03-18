# tango-rent-test

La prueba se divide en 2 carpetas correspondientes a las 2 partes de la prueba : 
* Frontend (Carpeta de prueba de la vista desarrollado con Vue 3)
* Backend (Carpeta de prueba del backend desarrollado en python 3)
# Vista :sunglasses:
<p align="center"><a target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Vue.js_Logo_2.svg/768px-Vue.js_Logo_2.svg.png?20170919082558" width="200"></a></p>

### Requisitos frontend

* Npm
* Nodejs

Para levantar la vista usted tendrá que ubicarse en la carpeta llamada frontend.

## Instalación de proyecto
### `npm install`
### Compilar y ejecutar la vista en el puerto local 8080
### `npm run dev`
# Backend :computer:
### Requisitos backend

* Python 3
* Selenium
* Numpy
* Pandas
* bs4
* openpyxl
* xlsxwriter
* Google Chrome
* Chrome driver

Para levantar el backend usted tendrá que ubicarse en la carpeta llamada backend. Tener instalado Google Chrome, y tener descargado su respectivo chrome driver ejecutable para su correspondiente sistema operativo y versión de google Chrome, y este ejecutable ubicarlo en la la misma carpeta. 

A su vez tendrá que editar la línea que tiene la ruta del driver de chrome: 

### `os.environ['PATH'] += r"C:/home/javierlopez/Documentos/fullstack-test-tango/backend/"`

Tambien tendrá que tener instaladas las bibliotecas indicadas mediante pip install. O el siguiente comando :

### `pip install selenium numpy pandas bs4 openpyxl xlsxwriter`

Una vez configurada las librerías y el driver de chrome, podra ejecutar el scrapper de python mediante : 

### `python3 scrapper.py`

# Notas sobre el backend

El backend utiliza código multiprocesos, por lo cual utuliza múltiples ventanas de chrone a la  vez, con un máximo de 3 ventanas al mismo tiempo. 

Tambien se implemento un backend de forma procecural imperativa con una sola ventana abierta, pero ese backend se demora aproximadamente 706 segundos (11 minutos). En cambio el backend multiprocesos se demora con 3 ventanas abiertas al mismo tiempo, al al rededor de 446 segundos, y con 4 ventanas abiertas 382 segundos, sin embargo debido a la potencia del equipo utilizado, cuando se utiliza las 4 ventanas a veces no se completa cada proceso, dedbido al uso excesivo de CPU y el programa falla, por lo cual se ha dejado en un máximo de 3 multi procesos, ya que asi se asegura al menos que se va a completar la operacion, aunque se demore 1 minuto más. 
