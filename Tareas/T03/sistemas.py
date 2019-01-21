import csv
from estructuras import ListaLigada
from entidades import Central, Elevadora, Transmision, Distribucion, Casa
from sistema import Sistema
from menu import Menu
from errores import InvalidQuery

class Red:
    def __init__(self, path):
        self.path = path
        self.sistemas = ListaLigada()
        self.centrales = ListaLigada()
        self.elevadoras = ListaLigada()
        self.transmisiones = ListaLigada()
        self.distribuciones = ListaLigada()
        self.casas = ListaLigada()
        self.cargar_datos(self.path)

    #### Funciones que cargan las bases de datos ####
    def cargar_datos(self, path):
        self.cargar_elevadoras(path)
        self.cargar_centrales(path)
        self.cargar_transmision(path)
        self.cargar_distribucion(path)
        self.cargar_casas(path)
        self.cargar_conexiones_transmision_elevadoras(path)
        self.cargar_conexiones_centrales_elevadoras(path)
        self.cargar_conexines_distribucion_transmision(path)
        self.cargar_conexiones_casas_distribucion(path)
        self.cargar_conexiones_casas_casas(path)

    def crear_sistema(self, sigla):
        sistema = Sistema(sigla)
        self.sistemas.agregar(sistema.sigla, sistema)
        return sistema

    def encontrar_sistema(self, sigla):
        for actual in self.sistemas:
            if actual.entidad.sigla == sigla:
                return actual.entidad
        return None

    def cargar_elevadoras(self, path):
        with open(path + 'elevadoras.csv', 'r', encoding='utf-8') as file:
            file.readline()
            line = Linked()
            reader = csv.reader(file)
            for line in reader:
                elevadora = Elevadora(*line)
                self.agregar_elevadora(elevadora)

    def cargar_centrales(self, path):
        with open(path + 'centrales.csv', 'r', encoding='utf-8') as file:
            file.readline()
            reader = csv.reader(file)
            for line in reader:
                central = Central(*line)
                self.agregar_central(central)

    def cargar_transmision(self, path):
        with open(path + 'transmision.csv', 'r', encoding='utf-8') as file:
            file.readline()
            reader = csv.reader(file)
            for line in reader:
                transmision = Transmision(*line)
                self.agregar_transmision(transmision)

    def cargar_distribucion(self, path):
        with open(path + 'distribucion.csv', 'r', encoding='utf-8') as file:
            file.readline()
            reader = csv.reader(file)
            for line in reader:
                distribucion = Distribucion(*line)
                self.agregar_distribucion(distribucion)

    def cargar_casas(self, path):
        with open(path + 'casas.csv', 'r', encoding='utf-8') as file:
            file.readline()
            reader = csv.reader(file)
            for line in reader:
                casa = Casa(*line)
                self.agregar_casa(casa)

    def cargar_conexiones_centrales_elevadoras(self, path):
        path += 'centrales_elevadoras.csv'
        with open(path, 'r', encoding='utf-8') as file:
            file.readline()
            reader = csv.reader(file)
            for line in reader:
                self.conectar_central_elevadora(*line)

    def cargar_conexiones_transmision_elevadoras(self, path):
        path += 'transmision_elevadoras.csv'
        with open(path, 'r', encoding='utf-8') as file:
            file.readline()
            reader = csv.reader(file)
            for line in reader:
                self.conectar_transmision_elevadora(*line)

    def cargar_conexines_distribucion_transmision(self, path):
        path += 'distribucion_transmision.csv'
        with open(path, 'r', encoding='utf-8') as file:
            file.readline()
            reader = csv.reader(file)
            for line in reader:
                self.conectar_distribucion_transmision(*line)

    def cargar_conexiones_casas_distribucion(self, path):
        path += 'casas_distribucion.csv'
        with open(path, 'r', encoding='utf-8') as file:
            file.readline()
            reader = csv.reader(file)
            for line in reader:
                self.conectar_casa_distribucion(*line)

    def cargar_conexiones_casas_casas(self, path):
        path += 'casas_casas.csv'
        with open(path, 'r', encoding='utf-8') as file:
            file.readline()
            reader = csv.reader(file)
            for line in reader:
                self.conectar_casa_casa(*line)

    ####   Funciones que agregan las entidades a los sistemas.
    def agregar_elevadora(self, elevadora):
        self.elevadoras.agregar(elevadora.id_, elevadora)
        sistema = self.encontrar_sistema(elevadora.sistema)
        if sistema is None:
            sistema = self.crear_sistema(elevadora.sistema)
        sistema.agregar_elevadora(elevadora)

    def agregar_central(self, central):
        self.centrales.agregar(central.id_, central)
        sistema = self.encontrar_sistema(central.sistema)
        sistema.agregar_central(central)

    def agregar_transmision(self, transmision):
        self.transmisiones.agregar(transmision.id_, transmision)
        sistema = self.encontrar_sistema(transmision.sistema)
        sistema.agregar_transmision(transmision)

    def agregar_distribucion(self, distribucion):
        self.distribuciones.agregar(distribucion.id_, distribucion)
        sistema = self.encontrar_sistema(distribucion.sistema)
        sistema.agregar_distribucion(distribucion)

    def agregar_casa(self, casa):
        self.casas.agregar(casa.id_, casa)
        sistema = self.encontrar_sistema(casa.sistema)
        sistema.agregar_casa(casa)

    # funciones que conectan los nodos
    def conectar_central_elevadora(self, id_central, id_elevadora, dist):
        central = self.centrales[id_central]
        if central is None:
            raise InvalidQuery(f'No existe Central con id {id_central}')
        elevadora = self.elevadoras[id_elevadora]
        if elevadora is None:
            raise InvalidQuery(f'No existe Elevadora con id {id_elevadora}')
        elevadora.conectar_central(central, float(dist))
        central.n_elevadoras += 1

    def conectar_transmision_elevadora(self, id_trans, id_elevadora, dist):
        elevadora = self.elevadoras[id_elevadora]
        if elevadora is None:
            raise InvalidQuery(f'No existe la Elevadora con id {id_elevadora}')
        transmision = self.transmisiones[id_trans]
        if transmision is None:
            raise InvalidQuery(f'No existe la Transmision con id {id_trans}')
        elevadora.agregar_conexion(transmision, float(dist))
        transmision.conectado = True

    def conectar_distribucion_transmision(self, id_dist, id_trans, dist):
        transmision = self.transmisiones[id_trans]
        if transmision is None:
            raise InvalidQuery(f'No existe Transmision con id {id_trans}')
        distribucion = self.distribuciones[id_dist]
        if distribucion is None:
            raise InvalidQuery(f'No existe Distribucion con id {id_dist}')
        transmision.agregar_conexion(distribucion, float(dist))
        distribucion.conectado = True

    def conectar_casa_distribucion(self, id_casa, id_dist, dist):
        distribucion = self.distribuciones[id_dist]
        if distribucion is None:
            raise InvalidQuery(f'No existe la Distribucion con id {id_dist}')
        casa = self.casas[id_casa]
        if casa is None:
            raise InvalidQuery(f'No existe la casa con id {id_casa}')
        distribucion.agregar_conexion(casa, float(dist))
        casa.conectado += 1

    def conectar_casa_casa(self, id_desde, id_hasta, dist):
        casa_desde = self.casas[id_desde]
        casa_hasta = self.casas[id_hasta]
        if casa_desde is None:
            raise InvalidQuery(f'No existe la casa con id {id_desde}')
        if casa_hasta is None:
            raise InvalidQuery(f'No existe la casa con id {id_hasta}')
        casa_desde.agregar_conexion(casa_hasta, float(dist))
        casa_hasta.conectado += 1

    # Funciones que eliminan nodos
    def eliminar_casa(self, id_):
        self.casas.eliminar(id_)
        casa = self.casas[id_]
        sistema = self.encontrar_sistema(casa.sigla)
        sistema.eliminar_casa(id_)

    def eliminar_distribucion(self, id_):
        self.distribuciones.eliminar(id_)
        distribucion = self.distribuciones[id_]
        sistema = self.encontrar_sistema(distribucion.sistema)
        sistema.eliminar_distribucion(id_)

    def eliminar_transmision(self, id_):
        self.transmisiones.eliminar(id_)

    def eliminar_nodos_sin_conexion(self):
        for sistema in self.sistemas:
            sistema.entidad.eliminar_nodos_sin_conexion()
        casas_a_eliminar = ListaLigada()
        for casa in self.casas:
            if not casa.entidad.conectado:
                casas_a_eliminar.agregar(casa.id_)
        for casa in casas_a_eliminar:
            self.casas.eliminar(casa.id_)
        distribuciones_a_eliminar = ListaLigada()
        for distribucion in self.distribuciones:
            if not distribucion.entidad.conectado:
                distribuciones_a_eliminar.agregar(distribucion.id_)
        for distribucion in distribuciones_a_eliminar:
            self.distribuciones.eliminar(distribucion.id_)
        transmisiones_eliminar = ListaLigada()
        for transmision in self.transmisiones:
            if not transmision.entidad.conectado:
                transmisiones_eliminar.agregar(transmision.id_)
        for transmision in transmisiones_eliminar:
            self.transmisiones.eliminar(transmision.id_)
        elevadoras_eliminar = ListaLigada()
        for elevadora in self.elevadoras:
            if not elevadora.entidad.conectado:
                elevadoras_eliminar.agregar(elevadora.id_)
        for elevadora in elevadoras_eliminar:
            self.elevadoras.eliminar(elevadora.id_)

    # funciones para consultas
    def potencia_real_red(self):
        potencia = 0
        for sistema in self.sistemas:
            potencia += sistema.entidad.potencia_real()
        return potencia

    def distribuciones_comuna(self, comuna):
        distribuciones_comuna = ListaLigada()
        actual = self.distribuciones.cabeza
        while actual is not None:
            d = actual.entidad
            if d.comuna == comuna:
                distribuciones_comuna.agregar(d.id_, d)
            actual = actual.siguiente
        if distribuciones_comuna.cabeza is None:
            return None
        return distribuciones_comuna  # tambien se puede retornar None si la lista está vacía.
