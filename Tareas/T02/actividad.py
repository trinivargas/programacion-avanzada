from abc import ABC, abstractmethod
from collections import deque
from math import pi
from parameters import η, κ, δ, ε, χ, ν
from random import randint

class Actividad(ABC):
    def __init__(self):
        super().__init__()
        self.esperando = deque()
        self.realizando = set()
        self.llegando = set()

    def destino(self, cliente):
        x, y = [10, cliente.x, 170], [150, cliente.y, 250]
        x.sort()
        y.sort()
        return x[1], y[1]

    @property
    def coordenadas_adentro(self):
        x = randint(10, 170)
        y = randint(150, 250)
        return x, y

    def duracion_actividad(self, c):
        return int(max(c.lucidez + c.sociabilidad - c.ansiedad, .1) * pi ** 2)

    @abstractmethod
    def permitir_actividad(self, cliente):
        pass

    @abstractmethod
    def llega_cliente(self, cliente):
        pass

    def vaciar(self):
        for cliente in set(self.esperando) | self.realizando | self.llegando:
            cliente.desocupar()


class Conversaciones(Actividad):
    def __init__(self):
        super().__init__()

    def destino(self, cliente):
        x, y = [240, cliente.x, 370], [150, cliente.y, 250]
        x.sort()
        y.sort()
        return x[1], y[1]

    @property
    def coordenadas_adentro(self):
        x = randint(240, 370)
        y = randint(150, 250)
        return x, y

    def permitir_actividad(self, cliente):
        return True

    def llega_cliente(self, cliente):
        self.llegando.add(cliente)
        cliente.actividad = 'yendo a la copucha'
        cliente.destino = self.destino(cliente)

    def tiempo_conversa(self, clientes):
        tiempos = map(self.duracion_actividad, clientes)
        return max(tiempos)

    def realizar(self, cliente):
        cliente.ansiedad -= ε / 100
        cliente.deshonestidad += χ
        cliente.converso = True

    def asignar_actividad(self, cliente, tiempo):
        cliente.tiempo_restante_actividad = tiempo
        cliente.actividad = 'conversar'
        self.realizando.add(cliente)


    def tick(self):
        clientes_llegaron = set()
        for cliente in self.llegando:
            if (cliente.x, cliente.y) == self.destino(cliente):
                clientes_llegaron.add(cliente)
                self.esperando.append(cliente)
        for cliente in clientes_llegaron:
            self.llegando.remove(cliente)

        # asigno pareja si existen dos o mas clientes esperando
        while len(self.esperando) >= 2:
            clientes = self.esperando.popleft(), self.esperando.popleft()
            tiempo = self.tiempo_conversa(clientes)
            self.asignar_actividad(clientes[0], tiempo)
            self.asignar_actividad(clientes[1], tiempo)
            x, y = self.coordenadas_adentro
            for i, cliente in enumerate(clientes):
                cliente.destino = x + (20 * i), y
                cliente.actividad = 'conversando'

        clientes_perkines = set()
        for cliente in self.esperando:
            cliente.tiempo_restante_actividad -= 1
            if cliente.tiempo_restante_actividad <= 0:
                clientes_perkines.add(cliente)

        for cliente in clientes_perkines:
            self.esperando.remove(cliente)
            cliente.desocupar()

        clientes_listos = set()
        for cliente in self.realizando:
            cliente.tiempo_restante_actividad -= 1
            if cliente.tiempo_restante_actividad <= 0:
                clientes_listos.add(cliente)

        for cliente in clientes_listos:
            self.realizar(cliente)
            self.realizando.remove(cliente)
            cliente.desocupar()


class TiniPadrino(Actividad):
    def __init__(self):
        super().__init__()
        self.ganancias = 0
        self.realizando = None

    def permitir_actividad(self, cliente):
        if cliente.dinero < 20:
            return False
        return True

    def llega_cliente(self, cliente):
        cliente.destino = self.destino(cliente)
        self.llegando.add(cliente)
        cliente.actividad = 'yendo a conversar con Tini'

    def realizar(self, cliente):
        cliente.dinero -= 20
        self.ganancias += 20
        cliente.stamina -= η
        cliente.hablo_con_tini += 1

    def vaciar(self):
        if self.realizando is not None:
            self.realizando.desocupar()

    def tick(self):
        clientes_llegaron = set()
        for cliente in self.llegando:
            if (cliente.x, cliente.y) == self.destino(cliente):
                self.esperando.append(cliente)
                clientes_llegaron.add(cliente)
                cliente.actividad = 'Esperando a Tini'
                cliente.destino = self.coordenadas_adentro
        for cliente in clientes_llegaron:
            self.llegando.remove(cliente)

        if self.realizando is None and self.esperando:
            cliente = self.esperando.popleft()
            self.realizando = cliente
            cliente.tiempo_restante_actividad = self.duracion_actividad(cliente)
            cliente.destino = self.coordenadas_adentro
            cliente.actividad = 'hablando con Tini'

        if self.realizando is None:
            return

        cliente = self.realizando
        cliente.tiempo_restante_actividad -= 1
        if cliente.tiempo_restante_actividad <= 0:
            self.realizar(cliente)
            cliente.desocupar()
            self.realizando = None


class Estudio(Actividad):
    def __init__(self):
        super().__init__()
        self.clientes_directo_ruleta = set()

    def permitir_actividad(self, cliente):
        if cliente.personalidad == 'kibitzer' and cliente.converso:
            return True
        return False

    def llega_cliente(self, cliente):
        self.llegando.add(cliente)
        cliente.actividad = 'yendo a estudiar'
        cliente.destino = 100, 200 #self.destino

    def tick(self):
        clientes_llegaron = set()
        for cliente in self.llegando:
            if (cliente.x, cliente.y) == self.destino(cliente):
                clientes_llegaron.add(cliente)
                self.realizando.add(cliente)
                cliente.tiempo_restante_actividad = self.duracion_actividad(
                    cliente)
                cliente.actividad = 'estudiando'
        for cliente in clientes_llegaron:
            self.llegando.remove(cliente)

        for cliente in self.realizando:
            cliente.tiempo_restante_actividad -= 1
            if cliente.tiempo_restante_actividad <= 0:
                cliente.fisico = True
                if random() <= cliente.deshonestidad:
                    cliente.rondas_trampas = ν
                    self.clientes_directo_ruleta.add(cliente)
                cliente.desocupar()

