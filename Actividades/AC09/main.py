import threading
import time
from itertools import chain
from random import randint


class Equipo(threading.Thread):  # join
    def __init__(self, equipo, ganador, nebil, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ganador = ganador
        self.nebil = nebil
        self.equipo = equipo
        self.hacker = Hacker(equipo)
        self.cracker = Cracker(equipo, self.nebil)

    def run(self):
        self.hacker.start()
        self.cracker.start()
        self.hacker.trabajando.wait()
        self.cracker.trabajando.wait()
        self.ganador.set()
        print(f'Gano el equipo {self.equipo}')


class Hacker(threading.Thread):
    def __init__(self, equipo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.equipo = equipo
        self.trabajando = threading.Event()
        self.termino = False

    def run(self):
        tiempo = randint(4, 12)
        time.sleep(tiempo)
        self.trabajando.clear()
        self.termino = True
        d = desencriptar('pista.txt')
        self.trabajando.set()
        print(f'Hacker del equipo {self.equipo} listo')


class Cracker(threading.Thread):
    def __init__(self,equipo ,nebil, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.equipo = equipo
        self.trabajando = threading.Event()
        self.lineas = 0
        self.problema = False
        self.nebil = nebil
        self.termino = False


    def run(self):
        while self.lineas < 50:
            if not self.problema:
                if not randint(0, 4):
                    self.problema = True
                else:
                    self.lineas += randint(5, 15)
            else:
                self.llamar_nebil()
            time.sleep(1)
        self.termino = True
        self.trabajando.set()
        print(f'Cracker del equipo {self.equipo} listo')

    def llamar_nebil(self):
        with self.nebil:
            print('Nebil, equipo', self.equipo, 'empezando')
            time.sleep(randint(1, 3))
            print('Nebil, equipo', self.equipo, 'terminando')
            self.problema = False


class Mision:
    def __init__(self, ):
        self.ganador = threading.Event()
        self.nebil = threading.Lock()
        self.crear_equipos()

    def crear_equipos(self):
        self.equipos = set()
        for i in range(3):
            e = Equipo(f'Team {i}', self.ganador, self.nebil)
            self.equipos.add(e)

    def run(self):
        for equipo in self.equipos:
            equipo.run()
        self.ganador.wait()

        for equipo in self.equipos:
            hacker_listo = equipo.hacker.termino
            cracker_listo = equipo.cracker.termino
            listo = {True: 'Si', False: 'No'}
            print(f'Equipo {equipo.equipo}:')
            print(f'Hacker listo: {listo[hacker_listo]}')
            print(f'Cracker listo: {listo[cracker_listo]}. '
                  f'Escribió {min(50, equipo.cracker.lineas)}')




def desencriptar(nombre_archivo):
    """
    Esta simple (pero útil) función te permite descifrar un archivo encriptado.
    Dado el path de un archivo, devuelve un string del contenido desencriptado.
    """

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        murcielago, numeros = "murcielago", "0123456789"
        dic = dict(chain(zip(murcielago, numeros), zip(numeros, murcielago)))
        return "".join(
            dic.get(char, char) for linea in archivo for char in linea.lower())


if __name__ == "__main__":
    mision = Mision()
    mision.run()


