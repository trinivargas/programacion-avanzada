import json
from datetime import datetime
from hashlib import blake2b

RECETAS_LOCK_PATH = 'RecetasLockJSON.json'
INGREDIENTES_PATH = 'ingredientes.txt'
'''
=====================================
NO BORRAR NI CAMBIAR!
'''
SUPER_SECRET_KEY = b'IIC2233'
'''
=====================================
'''


class Receta:
    """Clase que modela una receta del 'PyKitchen' cookbook"""

    def __init__(self, nombre='', ingredientes=None, alinos=None):
        self.nombre = nombre
        self.ingredientes = ingredientes or []
        self.alinos = alinos or []
        self.llave_segura = None

    @property
    def verificada(self):
        """Property que nos indica si una receta fue limpiada o no."""
        return hasattr(
            self, 'llave_segura') and self.llave_segura == self.encriptar()

    def encriptar(self):
        """Funcion que encripta el valor a partir de una llave secreta"""
        encriptador = blake2b(key=SUPER_SECRET_KEY, digest_size=16)
        encriptador.update(self.nombre.encode())

        return encriptador.hexdigest()

    @staticmethod
    def abrir_ingredientes():
        """Genera las líneas del archivo ingredientes.txt"""
        with open(INGREDIENTES_PATH, encoding='utf-8') as fp:
            yield from map(lambda x: x.strip(), fp)

    def abrir_recetas_lock(self):
        """
        Funcion para abrir el archivo que indica los atributos
        de las recetas
        """
        with open('RecetasLockJSON.json', encoding='utf-8') as file:
            return {atributo for atributo in json.load(file)}

    def __setstate__(self, state):  #deserialización
        """
        Deserializa

        Elimina los atributos incorrectos y los ingredientes inválidos.
        """
        nuevo = {key: value for key, value in state.items()
                 if key in self.abrir_recetas_lock()}
        ing = nuevo['ingredientes'] # lista de todos los ingredientes del state
        validos = set(self.abrir_ingredientes()) # agregar self
        ingredientes = [ingrediente for ingrediente in ing if ingrediente in validos]
        nuevo.update({"ingredientes": ingredientes})
        #nuevo.update({'verificada': True})
        self.__dict__ = nuevo


    def __getstate__(self): #serialización
        """
        Serializa

        Recuerda colocar el atributo llave_segura.
        """
        nuevo_dict = self.__dict__.copy()
        #nuevo_dict.update({"serializado": True})
        nuevo_dict.update({"llave_segura": self.encriptar()})
        return nuevo_dict


class Comida:
    def __init__(self,
                 nombre='',
                 nivel_preparacion=0.0,
                 ingredientes=None,
                 alinos=None,
                 fecha_ingreso=None):
        self.nombre = nombre
        if fecha_ingreso:
            segundos = (self.str_a_date(fecha_ingreso) - datetime.now()).seconds
            self.nivel_preparacion = nivel_preparacion + segundos/60
        self.ingredientes = ingredientes or []
        self.alinos = alinos or []

        ''' Recuerda cambiar aqui el nivel de preparacion de acuerdo a la fecha
        de ingreso!''' # a la preparacion sumar el n de minutos con

    @property
    def quemado(self):
        return self.nivel_preparacion > 100

    @property
    def preparado(self):
        return self.nivel_preparacion >= 100

    @staticmethod
    def date_a_str(fecha):
        return fecha.strftime('%Y-%m-%d-%H-%M-%S')

    @staticmethod
    def str_a_date(fecha_str):
        return datetime.strptime(fecha_str, '%Y-%m-%d-%H-%M-%S')

    @classmethod
    def de_receta(cls, receta):
        return cls(receta.nombre, 0.0, receta.ingredientes, receta.alinos)


class ComidaEncoder(json.JSONEncoder): # serializacíon
    """Utiliza esta clase para codificar en json """

    def default(self, obj):
        """Serializa en forma personalizada el tipo de objeto Comida"""

        if isinstance(obj, Comida):
            return {'nombre': obj.nombre,
                    'fecha_ingreso': obj.date_a_str(datetime.now()),
                    'nivel_preparacion': obj.nivel_preparacion,
                    'ingredientes': obj.ingredientes,
                    'alinos': obj.alinos}

        # Mantenemos la serialización por defecto para otros tipos
        return super().default(obj)

