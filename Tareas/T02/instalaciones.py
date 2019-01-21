from instalacion import Instalacion
from random import triangular, normalvariate, choice

#################################  Restobar  #################################

class Restobar(Instalacion):
    def __init__(self):
        super().__init__(20, 2)
        self.destino = 500, 150

    @property
    def coordenadas_adentro(self):
        x = choice([500, 540, 600, 640])
        return x, 100

    @property
    def funcionando(self):
        if len(self.personal) < 2:
            return False
        return True

    def duracion_por_persona(self, cliente=None):
        duracion = [10, int(70 / len(self.personal)), 50]
        duracion.sort()
        return duracion[1]

    def asistir(self, cliente):
        if cliente.lucidez > cliente.ansiedad:
            self._beber(cliente)
        elif cliente.lucidez < cliente.ansiedad:
            self._comer(cliente)
        else:
            choice([self._beber(cliente), self._comer(cliente)])
        self.cobrar(cliente)

    def _beber(self, cliente):
        cliente.lucidez -= .2
        cliente.ansiedad -= .15
        cliente.stamina += .15

    def _comer(self, cliente):
        cliente.lucidez += .1
        cliente.ansiedad -= .2


################################# Tarot  #################################

class Tarot(Instalacion):
    def __init__(self):
        super().__init__(1, 10)
        self.destino = 293, 106
        self.coordenadas_adentro = 293, 76

    @property
    def funcionando(self):
        return bool(len(self.personal))

    def duracion_por_persona(self, cliente=None):
        #return normalvariate(3, 5)
        return int(normalvariate(3, 5))

    def asistir(self, cliente):
        resultado = choice([0, 1])
        if resultado:
            cliente.stamina -= triangular(.01, .5, .1)
        else:
            cliente.suerte += triangular(.01, .3, .1)
        self.cobrar(cliente)


##################################  Baño  ##################################

class Bano(Instalacion):
    def __init__(self):
        super().__init__(20, .2)
        self.destino = 42, 300
        self.coordenadas_adentro = 42, 320

    @property
    def funcionando(self):
        return True

    def duracion_por_persona(self, cliente):
        return int(normalvariate(3 * (1 - cliente.lucidez), 2))

    def asistir(self, cliente):
        cliente.ansiedad -= .1
        self.cobrar(cliente)
