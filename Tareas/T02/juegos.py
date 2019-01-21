from instalacion import Instalacion
from parameters import α, γ, κ, ψ
from random import random, randint, choice
from abc import abstractmethod

class Juego(Instalacion):
    def __init__(self):
        super().__init__(20, 1)

    def apuesta(self, cliente):
        # se apuesta entre 1 y 2 sin pasar el maximo dinero del cliente
        apuesta = max(1, 1 + random() // 0.1)
        return min(apuesta, cliente.dinero)

    def probabilidad_ganar(self, cliente):
        return self.probabilidad_juego(cliente) + .2 * cliente.suerte - .1

    @abstractmethod
    def probabilidad_juego(self, cliente):
        pass

    def cobrar(self, cliente):
        pass


class Tragamonedas(Juego):
    def __init__(self):
        super().__init__()
        self.pozo = 0
        self.destino = 470, 280

    @property
    def coordenadas_adentro(self):
        x = choice([510, 530, 557, 580, 605, 630])
        y = choice([280, 330, 375])
        return x, y

    def duracion_por_persona(self, cliente):
        return 4

    @property
    def funcionando(self):
        return bool(self.personal)

    def probabilidad_juego(self, cliente=None):
        return α

    def asistir(self, cliente):
        apuesta = self.apuesta(cliente)
        self.ganancias += .1 * apuesta
        self.pozo += .9 * apuesta
        cliente.dinero -= apuesta
        if random() <= self.probabilidad_ganar(cliente):
            cliente.dinero += self.pozo
            self.pozo = 0


class Ruleta(Juego):
    def __init__(self):
        super().__init__()
        self.destino = 260, 290
        self.dinero_apostado = 0
        self.apuestas_clientes = {}
        self.clientes_tramposos = set()
        self.contadores_carta = set()

    @property
    def funcionando(self):
        if len(self.personal) > 0:
            return True
        return False

    def duracion_por_persona(self, cliente):
        ''' Cada ronda dura 3  minutos'''
        return 3

    @property
    def coordenadas_adentro(self):
        x = randint(295, 345)
        y = 315
        return x, y

    @property
    def dealer_coludido(self):
        for dealer in self.personal:
            if dealer.coludido:
                return True
        return False

    def probabilidad_juego(self, cliente):
        apostar = self.apostar()
        self.apuestas_clientes[cliente] = apostar
        if apostar == 'rojo' or apostar == 'negro':
            return γ/(2 * (γ + 1))
        return 1 / (γ + 1)

    def asistir(self, cliente):
        apuesta = self.apuesta(cliente)
        cliente.dinero -= apuesta
        self.ganancias += apuesta
        self.dinero_apostado += apuesta

        prob_ganar = self.probabilidad_ganar(cliente)

        ############
        # aumentar la probabilidad de ganar si es físico determinista
        if cliente.fisico and random() <= cliente.deshonestidad:
            self.contadores_carta.add(cliente)
            for dealer in self.personal:
                if dealer.descubrir_trampa:
                    self.clientes_tramposos.add(cliente)
                    return

            cliente.rondas_trampa -= 1
            prob_ganar += ψ

        # aumentar p de ganar si habló con Tini
        # por cada vez que habló con Tini aumenta la p de ganar
        if cliente.hablo_con_tini and self.dealer_coludido:
            prob_ganar += cliente.hablo_con_tini * κ / 100

        if random() <= prob_ganar:
            ap_cliente = self.apuestas_clientes[cliente]
            if ap_cliente == 'rojo' or ap_cliente == 'negro':
                cliente.dinero += 1.5 * apuesta
                self.ganancias -= 1.5 * apuesta
            else:
                cliente.dinero += 5 * apuesta
                self.ganancias -= 5 * apuesta

    def apostar(self):
        if randint(0, 1):
            return choice(['rojo', 'negro', 'verde'])
        return randint(0, γ)

    def _desocupar(self, clientes_desocupados):
        ''' En los juegos se puede jugar varias rondas, en cada una se apuesta
        y se puede ganar o perder plata'''
        for cliente in clientes_desocupados:
            self.asistir(cliente)

            # si ya no va a jugar más
            if cliente.rondas_juego <= 0:
                cliente.desocupar()
                self.n_clientes += 1
                self.clientes_instalacion.remove(cliente)

            # si todavia va a jugar
            else:
                cliente.rondas_juego -= 1
                cliente.tiempo_restante_actividad = \
                    self.duracion_por_persona(cliente)


