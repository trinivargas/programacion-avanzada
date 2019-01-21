from abc import ABC, abstractmethod


class Ser(ABC):
    def __init__(self, nombre, fuerza, resistencia, vida, ki):
        self.nombre = nombre
        self.fuerza = fuerza
        self.resistencia = resistencia
        self._vida = vida
        self.ki = ki

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, aumento):
        self._vida = sorted([0, self._vida + aumento])[1]

    @abstractmethod
    def atacar(self, enemigo):
        pass


class Humano(Ser):

    def __init__(self, *args, inteligencia=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.inteligencia = inteligencia

    def atacar(self, enemigo):
        vida_perdida = self.ki * (1 + self.fuerza - enemigo.resistencia)/2
        if vida_perdida <0:
            vida_perdida = 0

        print(f'{self.nombre} le quita {min(vida_perdida, enemigo.vida)} a {enemigo.nombre}')
        enemigo.vida -= vida_perdida

    def meditar(self):
        self.ki += self.inteligencia/100
        print(f'Yo {self.nombre} estoy meditando!')


class Extraterrestre(Ser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def atacar(self, enemigo):
        vida_perdida = self.ki * (1 + self.fuerza - enemigo.resistencia)
        if vida_perdida < 0:
            vida_perdida = 0

        self.fuerza = self.fuerza * 1.3
        print(f'{self.nombre} le quita {min(vida_perdida, enemigo.vida)} a {enemigo.nombre}')
        enemigo.vida += - vida_perdida



class Supersaiyayin(Extraterrestre, Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cola = True

    def perder_cola(self):
        if self.cola:
            self.cola = False
            self.resistencia = self.resistencia * 0.4



class Hakashi(Extraterrestre):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def robar_ki(self, *adversarios):
        for adversario in adversarios:
            ki_robado = 0.5 * adversario.ki
            adversario.ki -= ki_robado
            self.ki += ki_robado



if __name__ == '__main__':
    """
    A continuación debes instanciar cada uno de los objetos pedidos,
    para que puedas simular la batalla.
    """
    #print(help(Supersaiyayin))
    humano = Humano('Juan', 100, 100, 500, 40, inteligencia=200)
    supersaiayayin1 = Supersaiyayin('Yayin1', 100, 30, 50, 6)
    supersaiayayin2 = Supersaiyayin('Yayin2', 120, 70, 10, 13)
    hackashi1 = Hakashi('Kakashi1', 200, 200, 150, 40)
    hackashi2 = Hakashi('Kakashi2', 300, 1500, 50, 50)



