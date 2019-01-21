from entidades import Central, Elevadora, Transmision, Distribucion, Casa
from errores import InvalidQuery

class CreacionNodos:
    def __init__(self, principal, red):
        self.principal = principal
        self.red = red

    def menu(self):
        try:
            self._menu()
        except InvalidQuery:
            print('No ingresó una opción válida')
            self.menu()

    def _menu(self):
        opcion = '-1'
        while opcion != '0':
            print('\n¿Qué nodo quiere crear?\n(1) Casa\n(2) Distribucion\n(3) '
                  'Transmision\n(4) Elevadora\n(5) Central\n(0) Volver')
            opcion = self.principal.opcion(0, 5)
            if opcion == '1':
                self.crear_casa()
            elif opcion == '2':
                self.crear_distribucion()
            elif opcion == '3':
                self.crear_transmision()
            elif opcion == '4':
                self.crear_elevadora()
            elif opcion == '5':
                self.crear_central()

    ### Funciones para crear nodos
    def crear_casa(self):
        id_ = self.id_entidad(Casa, self.red.casas)
        sistema = self.pedir_sistema().sigla
        provincia = self.pedir_comuna_provincia('Provincia')
        comuna = self.pedir_comuna_provincia('Comuna')
        consumo = self.pedir_consumo('kW')
        casa = Casa(id_, sistema, provincia, comuna, consumo)
        self.red.agregar_casa(casa)

    def crear_distribucion(self):
        id_ = self.id_entidad(Distribucion, self.red.distribuciones)
        nombre = input('Nombre: ')
        sistema = self.pedir_sistema().sigla
        provincia = self.pedir_comuna_provincia('Provincia')
        comuna = self.pedir_comuna_provincia('Comuna')
        consumo = self.pedir_consumo('MW')
        distribucion = Distribucion(id_, nombre, sistema, provincia, comuna,
                                    consumo)
        self.red.agregar_distribucion(distribucion)

    def crear_transmision(self):
        id_ = self.id_entidad(Transmision, self.red.transmisiones)
        nombre = input('Nombre: ')
        sistema = self.pedir_sistema().sigla
        provincia = self.pedir_comuna_provincia('Provincia')
        comuna = self.pedir_comuna_provincia('Comuna')
        consumo = self.pedir_consumo('MW')
        transmision = Transmision(id_, nombre, sistema, provincia, comuna,
                                  consumo)
        self.red.agregar_transmision(transmision)

    def crear_elevadora(self):
        id_ = self.id_entidad(Elevadora, self.red.elevadoras)
        nombre = input('Nombre: ')
        sistema = self.pedir_sistema().sigla
        provincia = self.pedir_comuna_provincia('Provincia')
        comuna = self.pedir_comuna_provincia('Comuna')
        consumo = self.pedir_consumo('MW')
        elevadora =  Elevadora(id_, nombre, sistema, provincia, comuna, consumo)
        self.red.agregar_elevadora(elevadora)

    def crear_central(self):
        id_ = self.id_entidad(Central, self.red.centrales)
        nombre = input('Nombre: ')
        sistema = self.pedir_sistema().sigla
        provincia = self.pedir_comuna_provincia('Provincia')
        comuna = self.pedir_comuna_provincia('Comuna')
        tipo = self.pedir_tipo()
        potencia = self.pedir_potencia()
        central =  Central(id_, nombre, sistema, provincia, comuna, tipo,
                           potencia)
        self.red.agregar_central(central)

    ### Funciones para pedir parámetros
    def pedir_sistema(self):
        try:
            sistema = self._pedir_sistema()
        except InvalidQuery as err:
            print(err, 'No existe el sistema ' + err.razon)
            sistema = self.pedir_sistema()
        return sistema

    def _pedir_sistema(self):
        sigla = input('Sigla sistema eléctrico: ').upper()
        sistema = self.red.encontrar_sistema(sigla)
        if sistema is None:
            raise InvalidQuery(sigla)
        return sistema

    def id_entidad(self, entidad, existentes):
        entidad.id_ += 1
        while existentes[str(entidad.id_)]:
            entidad.id_ += 1
        print(f'id: {entidad.id_}')
        return str(entidad.id_)

    def pedir_comuna_provincia(self, tipo):
        try:
            comuna = self._pedir_comuna_provincia(tipo)
        except InvalidQuery as err:
            print(f'Nombre inválido para {tipo}')
            comuna = self.pedir_comuna_provincia(tipo)
        return comuna

    def _pedir_comuna_provincia(self, tipo):
        comuna = input(f'{tipo}: ').upper()
        if not comuna.replace(' ', '').isalpha():
            raise InvalidQuery(tipo)
        return comuna

    def pedir_consumo(self, unidad):
        try:
            consumo = self._pedir_consumo(unidad)
        except InvalidQuery as err:
            print('No ingresó un numero válido para consumo')
            consumo = self.pedir_consumo(unidad)
        return consumo

    def _pedir_consumo(self, unidad):
        consumo = input(f'Consumo en {unidad}: ')
        if not consumo.replace('.', '').isdigit() or consumo.count('.') > 1:
            raise InvalidQuery('Consumo')
        return consumo

    def pedir_tipo(self):
        try:
            tipo = self._pedir_tipo()
        except InvalidQuery as err:
            print(err, 'inválida')
            tipo = self.pedir_tipo()
        return tipo

    def _pedir_tipo(self):
        print('Ingrese el tipo de la central:\n(1) Solar\n(2) Termoelectrica'
              '\n(3) Biomasa')
        opcion = input('Opción: ')
        if opcion == '1':
            return 'Solar'
        elif opcion == '2':
            return 'Termoelectrica'
        elif opcion == '3':
            return 'Biomasa'
        else:
            raise InvalidQuery('Opción')

    def pedir_potencia(self):
        try:
            potencia = self._pedir_potencia()
        except InvalidQuery as err:
            if 'rango' in str(err):
                print('Rango inválido para potencia')
            else:
                print('Número inválido')
            potencia = self._pedir_potencia()
        return potencia

    def _pedir_potencia(self):
        print('Ingrese la potencia de la central. Debe ser un número entre 20 y'
              '200 MW')
        potencia = input('Potencia en MW: ')
        if not potencia.isdigit():
            raise InvalidQuery('Número')
        if not 20 <= float(potencia) <= 200:
            raise InvalidQuery('rango')
        return potencia