import json
import os
import os.path as path
import pickle

from clases import Comida, ComidaEncoder

BOOK_PATH = 'recetas.book'


class PyKitchen:
    def __init__(self):
        self.recetas = []
        self.comidas = []
        self.despachadas = []

    def cargar_recetas(self):
        '''Esta función se encarga de cargar el archivo recetas.book'''
        with open("recetas.book", 'rb') as file:
            self.recetas.extend(pickle.load(file))

    def guardar_recetas(self):
        '''Esta función se encarga de guardar las recetas (instancias), en el
        archivo recetas.book'''
        with open("recetas.book", 'rb') as file:
            pickle.dump(self.recetas, file)

    def cocinar(self):
        '''Esta funcion debe:
        - filtrar recetas verificadas
        - crear comidas a partir de estas recetas
        - guardar las comidas en la carpeta horno
        '''
        for receta in self.recetas:
            if receta.verificada:
                with open(os.path.join('horno', receta.nombre + '.json')) as file:
                    comida = Comida.de_receta(receta)
                    json.dump(comida, file, cls=ComidaEncoder)

    def despachar_y_botar(self):
        ''' Esta funcion debe:
        - Cargar las comidas que están en la carpeta horno.
            Pro tip: string.endswith('.json') retorna true si un string
            termina con .json
        - Crear instancias de Comida a partir de estas.
        - Guardar en despachadas las que están preparadas
        - Imprimir las comidas que están quemadas
        - Guardar en comidas las no preparadas ni quemadas
        '''
        for directorio in os.listdir(os.path.join(os.getcwd(), 'horno')):
            if directorio.endswith('.json'):
                with open(directorio, encoding='utf-8') as file:
                    comidas = json.load(file, object_hook=json_decoder)
                    self.comidas.extend(comidas)



