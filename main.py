""" 
Imagina que esta API es una biblioteca de peliculas:
La funcion load_movies() es como una biblioteca que carga el catalogo de libros (peliculas) cuando se abre la biblioteca.
La funcion get_movies() muestra todo el catalogo cuando alguien lo pide.
La funcion get_movie(id) es como si alguien preguntara por un libro especifico es decir, por un coidgo de identificacion.
La funcion chatbot (query) es un asistente que busca peliculas segun palabras clave y sinonimo.
La funcion get_movies_by_category(category) ayuda a encontrar peliculas segun su genero (accion, comedia, etc...)
"""
# Importamos las herramientas necesarias para continuar nuestra API
from fastapi import FastAPI, HTTPException # FastAPI nos ayuda a crear la API, HTTPException nos ayuda a manejar errores

from fastapi.responses import HTMLResponse, JSONResponse # HTMLResponse nos ayuda a manejar respuestas HTML, JSONResponse nos ayuda a manejar respuestas en formato JSON
import pandas as pd # pandas nos ayuda a manejar datos en tablas como si fuera un Excel
import nltk #nltk nos ayuda a procesar texto y analizar palabras.
from nltk.tokenize import word_tokenize #word_tokenize nos ayuda a tokenizar texto, es decir, a convertir texto en palabras.
from nltk.corpus import wordnet #wordnet nos ayuda a obtener sinonimos de una palabra.

# indicamos la ruta donde nltk buscara los datos desgargados en nuestro ckomputador

nltk.data.path.append(r'C:\Users\USUARIO\AppData\Roaming\nltk_data')
nltk.download('punkt_tab')
nltk.download('punkt') # es un paquete para dividir frases en palabras
nltk.download('wordnet') # paquete para encontrar sinonimos de palabras

# función para cargar las películas desde un archivo csv

def load_movies(): 
    # leemos el archivo que contiene inforamción del películas y seleccionamos las columnas más importantes
    df = pd.read_csv("./Dataset/netflix_titles.csv")[['show_id','title','release_year','listed_in','rating','description']]

    # renombramos las columnas para que sean más fáciles de entender
    df.columns = ['id','title','year','category','rating','overview']

    # llenamos los espacios vacios con texto vacio y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient='records')

# cargamos las películas al iniciar la API para no ller el archivo cada vez que alguien pregunte por ellas
movies_list = load_movies()

# funcion para encontrar sinónimos de una palabra
def get_synonyms(word):
    # usamos wirdnets para encontrar distintas palabras que significa lo mismo
    return{lemma.name().lower() for syn in wordnet.synsets(word) for lemma in syn.lemmas()}

# creamos la aplicación FastAPI que sera el motor de nuestre APPI
# esto inicializa la API con un nombre y una versión
app =  FastAPI(title='mi aplicación de películas', version='1.0.0')

@app.get('/', tags=['Home'])
def home():
    # cuando entremos en el navegador a http://127.0.0.1:8000 veremos un mensaje de bienvenida 
      return HTMLResponse('<h1> Bienvenido a la API de películas </h1>')

# # Obteniendo la lista de películas
# Creamos una ruta para obtener todas las películas
# Ruta para obtener todas las películas

@app.get('/movies', tags=['Movies'])
def get_movies():
    # Si hay películas, las enviamos, si no mostramos un error
    return movies_list or HTMLResponse(status_code=500, detail="No hay datos de películas disponibles")
 
# ruta para obtener una película específica por su ID
@app.get('/movies/{id}', tags=['Movies'])
def get_movies(id: str):
     # buscamos en la lista de películas la que tenga el mismo ID
     return next((m for m in movies_list if m ['id'] == id), {"detalle":"película no encontrada"})

# Ruta del chatbot que responde con películas segun palabras clave de la categoria
@app.get('/chatbot', tags=['chatbot'])
def chatbot(query: str):
    # Dividimos la consulta en palabras clave, para entender mejor la intension del usuario
    query_words = word_tokenize(query.lower())
    # Buscamos sinonimos de las palabras clave para ampliar la busqueda
    synonyms = {word for q in query_words for word in get_synonyms(q)} | set(query_words)
    
    # Filtramos la lista de peliculas buscando coinsidencias en la categoria
    results =[m for m in movies_list if any (s in m ['category'].lower() for s in synonyms)]
    
    # Si encontramos las peliculas, enviamos la lista de películas; sino, ostramos un mensaje de que no se encontraron cinsidencias
    
    return JSONResponse(content={
    "respuesta": "aqui tienes algunas peliculas relacionadas." if results else "no encontre peliculas en esa categoria.",
    "peliculas": results
    })
# ruta para busar películas por categoria específica

