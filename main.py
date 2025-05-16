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

nltk.data.bath.append ('c:\Users\USUARIO\AppData\Roaming\nltk_data')
nltk.download('punkt')