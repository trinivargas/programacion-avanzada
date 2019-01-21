from persona import Persona
from abc import ABC, abstractmethod
from random import triangular, normalvariate, random
from parameters import ω, Ω


class Personal(ABC, Persona):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad)
        self.proximo_turno = None

    @abstractmethod
    def tiempo_trabajo(self):
        pass

    @property
    def tiempo_descanso(self):
        t = [8, int(normalvariate(14, 5)), 20]
        t.sort()
        return t[1] * 60

    def _definir_proximo_turno(self, minutos_casino):
        tiempo = minutos_casino + self.tiempo_descanso * 60
        if not tiempo % 60:
            return tiempo
        return (tiempo // 60 + 1) * 60

    def descansar(self, minutos_casino):
        self.proximo_turno = self._definir_proximo_turno(minutos_casino)
        self.actividad = None

    def trabajar(self):
        self.tiempo_restante_actividad = self.tiempo_trabajo
        self.actividad = 'Trabajar'


class Bartender(Personal):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad)
        self.lugar_trabajo = 'Restobar'

    @property
    def tiempo_trabajo(self):
        return int(triangular(360, 540, 490))


class Dealer(Personal):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad)
        self.lugar_trabajo = 'Juegos'
        self.coludido = random() < Ω

    @property
    def tiempo_trabajo(self):
        return int(triangular(360, 540, 540))

    @property
    def descubrir_trampa(self):
        return random() <=  ω


class MrT(Personal):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad)
        self.lugar_trabajo = 'Tarot'

    @property
    def tiempo_trabajo(self):
        return int(triangular(360, 500, 420))