from personal import Bartender, MrT, Dealer
from cliente import Cliente
from instalaciones import Bano, Restobar, Tarot
from juegos import Tragamonedas, Ruleta
from actividad import Conversaciones , TiniPadrino, Estudio
from estadisticas import Estadisticas
from parameters import p
from random import choice, choices, randint, random
from gui.entities import Game, Building
import gui
from faker import Factory
from sys import exit


class DCCasino:

    def __init__(self, tiempo):
        self.tiempo = tiempo * 60  # se ingresa en minutos
        self.segundo = 0
        self.bano = Bano()
        self.restobar = Restobar()
        self.tarot = Tarot()
        self.ruleta = Ruleta()
        self.tragamonedas = Tragamonedas()
        self.conversaciones = Conversaciones()
        self.estudio = Estudio()
        self.tini_padrini = TiniPadrino()
        self.personal_libre_restobar = set()
        self.personal_libre_tarot = set()
        self.personal_libre_juegos = set()
        self.crear_personal()
        self.clientes = set()
        self.clientes_retiran = set()
        self.ganancias_total = 0
        self.diccionarios_estadisticas()

    def diccionarios_estadisticas(self):
        self.personalidad_clientes = {'millonario': [], 'ganador': [],
                                       'ludopata': [], 'kibitzer': [],
                                       'dieciochero': []}
        self.ganancias_personalidad = {'millonario': [], 'ganador': [],
                                       'ludopata': [], 'kibitzer': [],
                                       'dieciochero': []}
        self.tiempo_estadia = {'millonario': [], 'ganador': [], 'ludopata': [],
                               'kibitzer': [], 'dieciochero': []}
        self.razones_salida = {'decision': [], 'trampa': [], 'fin': []}

    def crear_personal(self):
        '''
        función que crea los 120 trabajadores del casino y crea el horario del
         primer turno de forma aleatoria entre las 20 primeras horas'''
        fake = Factory.create()

        for i in range(55):
            trabajador = Bartender(fake.name(), 40)
            trabajador.proximo_turno = randint(0, 20) * 60
            self.personal_libre_restobar.add(trabajador)
        for i in range(62):
            trabajador = Dealer(fake.name(), 45)
            trabajador.proximo_turno = randint(0, 20) * 60
            self.personal_libre_juegos.add(trabajador)
        for i in range(3):
            trabajador = MrT(fake.name(), 48)
            trabajador.proximo_turno = 6 * i * 60 # en minutos
            self.personal_libre_tarot.add(trabajador)

    def agregar_personal_instalacion(self, trabajador, instalacion):
        instalacion.llega_trabajador(trabajador)

    def empezar_turno_personal(self, minuto):
        ''' función que agrega los trabajadores que empiezan el turno en el
        minuto dado'''

        for trabajador in self.personal_libre_restobar:
            if trabajador.proximo_turno == minuto:
                self.restobar.llega_trabajador(trabajador)

        for trabajador in self.personal_libre_tarot:
            if trabajador.proximo_turno == minuto:
                self.tarot.llega_trabajador(trabajador)

        for trabajador in self.personal_libre_juegos:
            if trabajador.proximo_turno == minuto:
                # agregar el trabajador al juego que tenga menos personal
                if len(self.tragamonedas.personal) <= len(self.ruleta.personal):
                    self.tragamonedas.llega_trabajador(trabajador)
                else:
                    self.ruleta.llega_trabajador(trabajador)

    def terminar_turno_personal(self, minuto):
        ''' termina turno de cada tipo de personal y empieza el turno de
        descanso '''
        personal_libre = self.restobar.tick_personal()
        for trabajador in personal_libre:
            self.personal_libre_restobar.add(trabajador)
            trabajador.descansar(minuto)

        personal_libre = self.tarot.tick_personal()
        for trabajador in personal_libre:
            self.personal_libre_restobar.add(trabajador)
            trabajador.descansar(minuto)

        personal_libre1 = self.tragamonedas.tick_personal()
        personal_libre2 = self.ruleta.tick_personal()
        for trabajador in personal_libre1 | personal_libre2:
            self.personal_libre_juegos.add(trabajador)
            trabajador.descansar(minuto)

    def llega_cliente(self):
        ''' funcion que dada una probabilidad crea un cliente y lo agrega a
         los clientes libres del casino'''
        if random() <= p:
            personalidad = choice(['ludopata', 'kibitzer', 'dieciochero',
                                   'ganador', 'millonario'])
            fake = Factory.create()
            cliente = Cliente(fake.name() , randint(18, 80), personalidad)
            cliente.x, cliente.y = -5, -20
            self.clientes.add(cliente)
            cliente.ingreso = self.segundo
            gui.add_entity(cliente)

    def tomar_decision(self, cliente):
        retirarse = 1 - cliente.stamina
        jugar = min(cliente.ansiedad, 1 - retirarse)
        actividad = min(cliente.sociabilidad, 1 - retirarse - jugar)
        instalacion = 1 - retirarse - actividad - jugar
        return choices(['retirarse', 'jugar', 'actividad', 'instalacion'],
                       [retirarse, jugar, actividad, instalacion])[0]

    def asignar_actividad(self):
        for cliente in self.clientes:
            if not cliente.ocupado:
                decision = self.tomar_decision(cliente)
                if decision == 'retirarse':
                    self.razones_salida['decision'].append(1)
                    self.clientes_retiran.add(cliente)
                elif decision == 'instalacion':
                    self.ir_instalacion(cliente)
                elif decision == 'jugar':
                    self.jugar(cliente)
                elif decision == 'actividad':
                    self.realizar_actividad(cliente)


    def realizar_actividad(self, cliente):
        eleccion = choice(['conversar', 'estudiar', 'Tini'])
        #eleccion = 'conversar' ########### Borrar
        actividades = {'conversar': self.conversaciones,
                       'estudiar': self.estudio, 'Tini': self.tini_padrini}
        actividad = actividades[eleccion]
        if actividad.permitir_actividad(cliente):
            self.agregar_cliente_instalacion(cliente, actividad)

    def ir_instalacion(self, cliente):
        eleccion = choice(['restobar', 'tarot', 'baño'])
        instalaciones = {'restobar': self.restobar, 'tarot': self.tarot,
                         'baño': self.bano}
        instalacion = instalaciones[eleccion]
        if instalacion.permitir_ingreso(cliente):
            self.agregar_cliente_instalacion(cliente, instalacion)

    def jugar(self, cliente):
        eleccion = choice(['ruleta', 'tragamonedas'])
        juegos = {'ruleta': self.ruleta, 'tragamonedas': self.tragamonedas}
        juego = juegos[eleccion]
        if juego.permitir_ingreso(cliente):
            self.agregar_cliente_instalacion(cliente, juego)

    def agregar_cliente_instalacion(self, cliente, instalacion):
        ''' agrega un cliente a una instalacion, juego o actividad'''
        instalacion.llega_cliente(cliente)

    def retirar_cliente_casino(self, cliente):
        ''' esta funcion no deberia afectar el set de clientes libres'''
        self.clientes.remove(cliente)
        cliente.destino = -5, -30
        cliente.deleteLater()

        # sacar cliente de la interfaz y recolectar estadísticas
        self._registrar_ganancias(cliente)
        self._registrar_tiempo_estadia(cliente)
        self._registrar_personalidad(cliente)

    def _registrar_personalidad(self, cliente):
        personalidad = cliente.personalidad
        self.personalidad_clientes[personalidad].append(1)

    def _registrar_ganancias(self, cliente):
        gasto = cliente.dinero - cliente.dinero_inicial
        self.ganancias_personalidad[cliente.personalidad].append(gasto)

    def _registrar_tiempo_estadia(self, cliente):
        tiempo = (self.segundo - cliente.ingreso)/ 60 # en minutos
        self.tiempo_estadia[cliente.personalidad].append(tiempo)

    def tick(self):
        # las decisiones se toman cada minuto
        if not self.segundo % 60:
            self._tick(self.segundo // 60)
        self.segundo += 1

        for instalacion in self.instalaciones.values():
            instalacion.angle += 0

        for cliente in self.clientes:
            cliente.angle += 0
            x, y = cliente.destino
            self._ir_coordenada(cliente, x, y)

        if self.segundo == self.tiempo:
            self._terminar_simulacion()

    def _tick(self, minuto):
        if not minuto % 50:
            print(minuto)
        self.empezar_turno_personal(minuto)
        self.terminar_turno_personal(minuto)

        # llegan clientes y a los libres se le asigna una actividad
        self.llega_cliente()
        self.asignar_actividad()

        for cliente in self.clientes_retiran:
            self.retirar_cliente_casino(cliente)
        self.clientes_retiran = set()

        # tick de las instalaciones / actividades / juegos
        self.restobar.tick_clientes()
        self.tarot.tick_clientes()
        self.bano.tick_clientes()
        self.ruleta.tick_clientes()
        self.tragamonedas.tick_clientes()
        self.conversaciones.tick()
        self.estudio.tick()
        self.tini_padrini.tick()

        for cliente in self.ruleta.clientes_tramposos:
            self.clientes.remove(cliente)
            self.retirar_cliente_casino(cliente)
            self.razones_salida['trampa'].append(1)
        self.ruleta.clientes_tramposos = set()

        for cliente in self.estudio.clientes_directo_ruleta:
            if self.ruleta.permitir_ingreso(cliente):
                self.ruleta.llega_cliente(cliente)
        self.estudio.clientes_directo_ruleta = set()

    def _ir_coordenada(self, cliente, x, y):
        if cliente.x - x > 0:
            cliente.x -= 1
        elif cliente.x - x < 0:
            cliente.x += 1
        if cliente.y - y > 0:
            cliente.y -= 1
        elif cliente.y - y < 0:
            cliente.y += 1

    def simulacion(self):
        gui.init()
        gui.set_size(773, 485)
        restobar = Building('restobar', 550, 40)
        tarot = Building('tarot', 310, 40)
        banos = Building('baños', 70, 370)
        tragamonedas = Game('tragamonedas', 550, 300)
        ruleta = Game('ruleta', 300, 370)
        self.instalaciones = {'restobar': restobar, 'tarot': tarot,
                              'bano': banos, 'tragamonedas': tragamonedas,
                              'ruleta': ruleta}

        for instalacion in self.instalaciones.values():
            gui.add_entity(instalacion)

        if self.segundo <= self.tiempo:
            gui.run(self.tick, 5)

    def _terminar_simulacion(self):
        clientes = {c for c in self.clientes}
        for cliente in clientes:
            self.retirar_cliente_casino(cliente)
            self.razones_salida['fin'].append(1)
        statistics = Estadisticas(self)
        print(statistics.resultados())
        exit()
