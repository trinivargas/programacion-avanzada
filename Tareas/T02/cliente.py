from persona import Persona
from collections import namedtuple
from random import uniform
from gui.entities import Human


Personalidad = namedtuple('Personalidad', 'dinero lucidez ansiedad suerte '
                                          'sociabilidad stamina deshonestidad')


class Cliente(Persona, Human):

    def __init__(self, nombre, edad, personalidad):
        super().__init__(nombre, edad, personalidad)
        self.personalidad = personalidad
        self._definir_atributos()
        self.converso = False
        self.hablo_con_tini = 0
        self.destino = (-5, -20)
        self.fisico = False
        self.rondas_juego = 0
        self.ingreso = 0

    def _opciones_personalidad(self):
        ''' funcion que retorna '''
        A = lambda: uniform(.7, 1)
        M = lambda: uniform(.3, .7)
        B = lambda: uniform(0, .3)
        p = {'ludopata': Personalidad(M, M, A, M, M, A, M),
             'kibitzer': Personalidad(B, M, B, M, A, B, M),
             'dieciochero': Personalidad(M, B, A, M, A, M, B),
             'ganador': Personalidad(M, M, M, A, A, A, A),
             'millonario': Personalidad(A, M, M, M, M, A, M)}
        return p[self.personalidad]

    def _definir_atributos(self):
        personalidad = self._opciones_personalidad()
        self.dinero_inicial = personalidad.dinero() * 200
        self.dinero = self.dinero_inicial
        self.lucidez = personalidad.lucidez()
        self._ansiedad = personalidad.ansiedad()
        self.suerte = personalidad.suerte()
        self.sociabilidad = personalidad.sociabilidad()
        self._stamina = personalidad.stamina()
        self.deshonestidad = personalidad.deshonestidad()

    @property
    def ansiedad(self):
        if .2 * self.dinero_inicial < self.dinero < 2 * self.dinero_inicial:
            return 1.25 * self._ansiedad
        return self._ansiedad

    @ansiedad.setter
    def ansiedad(self, value):
        self._ansiedad += value

    @property
    def stamina(self):
        if not self.dinero:
            self._stamina = 0
            return 0
        return self._stamina

    @stamina.setter
    def stamina(self, value):
        stamina = [0, self.stamina + value, 1]
        stamina.sort()
        self._stamina = stamina[1]

