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

### Requisitos backend

* Python 3
* Selenium
* Numpy
* Pandas
* bs4
* Google Chrome
* Chrome driver

Para levantar el backend usted tendrá que ubicarse en la carpeta llamada backend. Tener instalado Google Chrome, y tener descargado su respectivo chrome driver ejecutable para su correspondiente sistema operativo y versión de google Chrome, y este ejecutable ubicarlo en la la misma carpeta. 

A su vez tendrá que editar la línea que tiene la ruta del driver de chrome: 

### `os.environ['PATH'] += r"C:/home/javierlopez/Documentos/fullstack-test-tango/backend/"`

Tambien tendrá que tener instaladas las bibliotecas indicadas mediante pip install. O el siguiente comando :

### `pip install selenium numpy pandas bs4`

Una vez configurada las librerías y el driver de chrome, podra ejecutar el scrapper de python mediante : 

### `python3 main.py`
