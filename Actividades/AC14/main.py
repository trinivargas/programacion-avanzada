import json
import re
from time import sleep
from os import path

import requests

from credenciales import API_KEY


API_URL = "https://api.nasa.gov/planetary/apod"
DIR_IMAGENES = 'imagenes'
PATH_RESULTADOS = 'resultados.txt'


def limpiar_fecha(linea):
    '''
    Esta función se encarga de limpiar el texto introducido a las fechas

    :param linea: str
    :return: str
    '''
    return re.sub('</?\w+>', '', linea)



def chequear_fecha(fecha):
    '''
    Esta función debe chequear si la fecha cumple el formato especificado

    :param fecha: str
    :return: bool
    '''
    return bool(re.fullmatch('\d{4}-\d{2}-\d{2}', fecha))


def obtener_fechas(path):
    '''
    Esta función procesa las fechas para devolver aquellas que son útiles
    para realizar las consultas a la API

    :param path: str
    :return: iterable
    '''
    fechas = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            fecha = limpiar_fecha(line.strip())
            if chequear_fecha(fecha):
                fechas.append(fecha)
    return fechas


def obtener_info(fecha):
    '''
    Recibe una fecha y retorna un diccionario
    con el título, la fecha y el url de la imagen
    :param fecha: str
    :return: dict
    '''
    url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(url, params={'date': fecha, 'hd': False,
                                         'api_key': API_KEY})
    # retorna titulo, fecha y url
    info = response.json()
    title = info['title']
    date = info['date']
    image_url = info['url']
    return {'title': title, 'date': date, 'url': image_url}


def escribir_respuesta(datos):
    '''
    Esta función debe escribir las respuestas de la API en el archivo
    resultados.txt

    :param datos_respuesta: dict
    '''
    url = datos['url']
    with open('resultados.txt', 'a', encoding='utf-8') as file:
        file.write(f'{datos["date"]} --> {datos["title"]}: {url}\n')

    name = re.split('/', url)[-1]
    descargar_imagen(url, path.join('imagenes', name))



def descargar_imagen(url, path):
    '''
    Recibe la url de una imagen y guarda los datos en un archivo en path

    :param url: str
    :param path: str
    '''
    respuesta = requests.get(url, stream=True)
    if respuesta.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in respuesta:
                f.write(chunk)


if __name__ == "__main__":
    PATH_FECHAS = 'fechas_secretas.txt'
    for fecha in obtener_fechas(PATH_FECHAS):
        respuesta = obtener_info(fecha)
        escribir_respuesta(respuesta)
