from estructuras import ListaLigada, Nodo
from errores import ForbidenAction, ElectricalOverload
ρ = 0.0172

class Casa:
    id_ = 0

    def __init__(self, id_, sist_electrico, provincia, comuna, consumo):
        self.nombre = 'Casa'
        self.id_ = id_
        Casa.id_ += 1
        self.sistema = sist_electrico
        self.provincia = provincia
        self.comuna = comuna
        self.consumo = float(consumo) / 1000
        self.conexiones = ListaLigada()
        self.conectado = 0
        self.p_ideal = 0
        self.p_real = 0

    @property
    def potencia(self):
        potencia = self.consumo
        for casa in self.conexiones:
            resistencia = ρ * casa.distancia / 85
            potencia_conexion = casa.entidad.potencia / casa.entidad.conectado
            potencia += potencia_conexion / (1 - resistencia)
        self.p_ideal = potencia
        return potencia # en MW

    def agregar_conexion(self, casa, distancia):
        if not isinstance(casa, Casa):
            razon = f'entre Casa y {casa.nombre}'
            raise ForbidenAction('agregar_arista', razon)
        if self.id_ == casa.id_:
            raise ForbidenAction('agregar_arista', 'porque se forma un ciclo.')
        self.crea_ciclo(casa)
        '''if self.conexion is not None: # creo que hay que cambiar esto
            return # raise algun Error'''
        if self.comuna != casa.comuna:
            porque = 'entre casas de distintas comunas.'
            raise ForbidenAction('agregar_arista', porque)
        self.conexiones.agregar(casa.id_, casa, distancia)

    def eliminar_conexion(self, id_):
        self.conexiones.eliminar(id_)

    def eliminar_conexiones(self):
        if not self.conectado:
            for casa in self.conexiones:
                casa.conectado = max(0, casa.conectado - 1)
                casa.eliminar_conexiones()
            self.conexiones = ListaLigada()

    def potencia_real(self):
        p_ideal_repartir = self.p_ideal - self.consumo
        p_real_repartir = max(0, self.p_real - self.consumo)
        for casa in self.conexiones:
            c = casa.entidad
            if self.p_ideal == self.p_real:
                c.p_real += c.p_ideal / c.conectado
            elif not p_real_repartir:
                c.p_real += 0
            else:
                p_ideal_c = c.p_ideal / (1 - (ρ * casa.distancia / 85))  # incluye la que se pierde en el camino
                x_c = p_real_repartir * p_ideal_c / p_ideal_repartir
                c.p_real += max(0, x_c - x_c * ρ * casa.distancia / 85)
            if c.p_real >= 30:
                raise ElectricalOverload(c.p_real * 1000)
            c.potencia_real()

    def crea_ciclo(self, casa2):
        nodos_hijos_casa_2 = casa2.nodos_hijos()
        if nodos_hijos_casa_2.en(self.id_):
            raise ForbidenAction('agregar_arista', 'se forma un ciclo')

    def nodos_hijos(self):
        visitados = ListaLigada()
        cola = ListaLigada()
        cola.agregar(self.id_, self)
        while cola:
            vertice = cola.popleft()  # es una instancia de alguna entidad
            if vertice is not None and not visitados.en(vertice.id_):
                visitados.agregar(vertice.id_, vertice)
                for v in vertice.conexiones:
                    if isinstance(v, Nodo):
                        v = v.entidad
                    if not visitados.en(v.id_):
                        cola.agregar(v.id_, v)
        return visitados

    def __str__(self):
        return f'Casa {self.id_}, sistema: {self.sistema}'


class Distribucion:
    id_ = 0

    def __init__(self, id_, nombre, sist_electrico, provincia, comuna, consumo):
        self.id_ = id_
        self.nombre = 'Distribucion'
        Distribucion.id_ += 1
        self.nombre = nombre
        self.sistema = sist_electrico
        self.provincia = provincia
        self.comuna = comuna
        self.consumo = float(consumo)
        self.conexiones = ListaLigada()
        self.conectado = False
        self.p_ideal = 0
        self.p_real = 0

    def agregar_conexion(self, casa, distancia):
        if not isinstance(casa, Casa):
            razon = f'entre Distribucion y {casa.nombre}'
            raise ForbidenAction('agregar_arista', razon)
        if self.comuna != casa.comuna:
            razon = 'entre Distribucion y Casa de distintas comunas.'
            raise ForbidenAction('agregar_arista', razon)
        self.conexiones.agregar(casa.id_, casa, distancia)

    def eliminar_conexion(self, id_):
        self.conexiones.eliminar(id_)

    def eliminar_conexiones(self):
        for casa in self.conexiones:
            casa.conectado = max(0, casa.conectado - 1)
            casa.eliminar_conexiones()
        self.conexiones = ListaLigada()

    @property
    def potencia(self):
        potencia = self.consumo
        for casa in self.conexiones:
            c = casa.entidad
            resistencia = ρ * casa.distancia / 85
            potencia += c.potencia / (1 - resistencia)
        self.p_ideal = potencia
        return potencia

    def potencia_real(self):
        p_ideal_repartir = self.p_ideal - self.consumo
        p_real_repartir = max(0, self.p_real - self.consumo)
        for casa in self.conexiones:
            c = casa.entidad
            if self.p_ideal == self.p_real:
                c.p_real += c.p_ideal / c.conectado
            elif not p_real_repartir:
                c.p_real += 0
            else:
                p_ideal_c = c.p_ideal / (1 - (ρ * casa.distancia / 85))  # incluye la que se pierde en el camino
                x_c = p_real_repartir * p_ideal_c / p_ideal_repartir
                c.p_real += max(0, x_c - x_c * ρ * casa.distancia / 85)
            if c.p_real > 30:
                raise ElectricalOverload(c.p_real * 1000)
            c.potencia_real()

    def nodos_hijos(self, id_=None):
        visitados = ListaLigada()
        cola = ListaLigada()
        cola.agregar(self.id_, self)
        while cola:
            vertice = cola.popleft()  # es una instancia de alguna entidad
            if vertice is not None and not visitados.en(vertice.id_):
                visitados.agregar(vertice.id_, vertice)
                if id_ is not None and vertice.id_ == id_:
                    return visitados
                for v in vertice.conexiones:
                    if isinstance(v, Nodo):
                        v = v.entidad
                    if not visitados.en(v.id_):
                        cola.agregar(v.id_, v)

        return visitados

    def __str__(self):
        return f'Distribución {self.id_}, sistema: {self.sistema}'


class Transmision:
    id_ = 0

    def __init__(self, id_, nombre, sist_electrico, provincia, comuna, consumo):
        self.nombre = 'Transmision'
        Transmision.id_ += 1
        self.id_ = id_
        self.nombre = nombre
        self.sistema = sist_electrico
        self.provincia = provincia
        self.comuna = comuna
        self.consumo = float(consumo)
        self.conexiones = ListaLigada()
        self.conectado = False
        self.p_ideal = 0
        self.p_real = 0

    def agregar_conexion(self, distribucion, distancia):
        if not isinstance(distribucion, Distribucion):
            razon = f'entre Transmision y {distribucion.nombre}.'
            raise ForbidenAction('agregar_arsita', razon)
        if self.provincia != distribucion.provincia:
            razon = 'entre Transmision y Distribucion de distintas provincias.'
            raise ForbidenAction('agregar_arista', razon)
        self.conexiones.agregar(distribucion.id_, distribucion, distancia)

    def eliminar_conexion(self, id_):
        self.conexiones.eliminar(id_)

    def eliminar_conexiones(self):
        for dist in self.conexiones:
            dist.conectado = False
            dist.eliminar_conexiones()
        self.conexiones = ListaLigada()

    @property
    def potencia(self):
        potencia = self.consumo
        for distribucion in self.conexiones:
            d = distribucion.entidad
            resistencia = ρ * distribucion.distancia / 152
            potencia += d.potencia / (1 - resistencia)
        self.p_ideal = potencia
        return potencia

    def potencia_real(self):
        # hay tres casos: (1) si llega la potencia necesaria
        # (2) si no llega nada de potencia (3) llega menos de la necesaria
        p_ideal_repartir = self.p_ideal - self.consumo
        p_real_repartir = max(0, self.p_real - self.consumo)

        for distribucion in self.conexiones:
            d = distribucion.entidad
            if self.p_ideal == self.p_real:
                d.p_real = d.p_ideal
            elif not p_real_repartir:
                d.p_real = 0
            else:
                p_ideal_d = d.p_ideal / (1 - (ρ * distribucion.distancia / 152))  # incluye la que se pierde en el camino
                x_d = p_real_repartir * p_ideal_d / p_ideal_repartir
                d.p_real = max(0, x_d - x_d * ρ * distribucion.distancia / 152)
            d.potencia_real()

    def __str__(self):
        return f'Transmision {self.id_}, sistema: {self.sistema}'


class Elevadora:
    id_ = 0

    def __init__(self, id_, nombre, sist_electrico, provincia, comuna, consumo):
        self.nombre = 'Elevadora'
        Elevadora.id_ += 1
        self.id_ = id_
        self.nombre = nombre
        self.sistema = sist_electrico
        self.provincia = provincia
        self.comuna = comuna
        self.consumo = float(consumo)
        self.centrales = ListaLigada()
        self.conexiones = ListaLigada()
        self.conectado = False
        self.p_ideal = 0
        self.p_real = 0

    @property
    def potencia(self):
        '''
        property que retorna la potencia ideal de cada entidad considerando los
        nodos hijos. '''
        potencia = self.consumo
        for transmision in self.conexiones:
            t = transmision.entidad
            resistencia = ρ * transmision.distancia / 202.7
            potencia += t.potencia / (1 - resistencia)
        self.p_ideal = potencia
        return potencia

    @property
    def potencia_recibida(self):
        potencia = 0
        for central in self.centrales:
            c = central.entidad
            potencia += max(0, c.potencia - ρ * central.distancia / 253)
        return potencia

    def potencia_real(self):
        ''' define la potencia real que llega a los nodos hijos'''
        # primero volvemos a definir la potencia ideal de cada nodo
        p_ideal_repartir = self.potencia - self.consumo # en otros casos es self.p_ideal # es la potencia que deberia repartir en totas
        self.p_real = self.potencia_recibida
        p_real_repartir = max(0, min(self.p_real - self.consumo, self.p_ideal)) # en otros casos es self.p_real # es la potencia que va a repartir en total
        # se calcula lo que se gasta en cada transmision, y el % que representa
        for transmision in self.conexiones:
            t = transmision.entidad
            if p_real_repartir >= self.p_ideal:
                t.p_real = t.p_ideal
            elif p_real_repartir > 0:
                # potencia que la elevadora debería destinar a t
                p_ideal_t = t.p_ideal / (1 - ρ * transmision.distancia / 202.7) # incluye la que se pierde en el camino
                x_t = p_real_repartir * p_ideal_t / p_ideal_repartir
                t.p_real = max(0, x_t - x_t * ρ * transmision.distancia/ 202.7) # lo que se pierde es la resistencia * potencia
            else:
                t.p_real = 0
            t.potencia_real()

    def agregar_conexion(self, transmision, distancia):
        if not isinstance(transmision, Transmision):
            razon = f'entre Elevadora y {transmision.nombre}.'
            raise ForbidenAction('agregar_arista', razon)
        if self.existe_transmision_provincia(transmision.provincia):
            razon = f'porque ya existe una Transmision en la provincia ' \
                    f'{transmision.provincia}'
            raise ForbidenAction('agregar_arista', razon)
        self.conexiones.agregar(transmision.id_, transmision, distancia)

    def eliminar_conexion(self, id_):
        self.conexiones.eliminar(id_)

    def eliminar_conexiones(self):
        for trans in self.conexiones:
            trans.conectado = False
            trans.eliminar_conexiones()
        self.conexiones = ListaLigada()

    def conectar_central(self, central, distancia):
        if not isinstance(central, Central):
            razon = f'entre Elevadora y {central.nombre}.'
            raise ForbidenAction('agregar_arista', razon)
        if not central.sistema == self.sistema:
            razon = 'entre Elevadora y Central de distintos sistemas.'
            raise ForbidenAction('agregar_nodo', razon)
        self.centrales.agregar(central.id_, central, distancia)

    def eliminar_conexion_central(self, id_):
        self.centrales.eliminar(id_)

    def existe_transmision_provincia(self, provincia):
        for transmision in self.conexiones:
            if transmision.entidad.provincia == provincia:
                return True
        return False

    def __str__(self):
        return f'Elevadora {self.id_}, sistema: {self.sistema}'


class Central:
    id_ = 0

    def __init__(self, id_, nombre, sistema, provincia, comuna, tipo, potencia):
        self.nombre = 'Central'
        Central.id_ += 1
        self.id_ = id_
        self.nombre = nombre
        self.sistema = sistema
        self.provincia = provincia
        self.comuna = comuna
        self.tipo = tipo
        self._potencia = float(potencia)
        self.n_elevadoras = 0

    @property
    def potencia(self):
        if not self.n_elevadoras:
            return 0
        return self._potencia / self.n_elevadoras

    def __str__(self):
        return f'Central {self.id_}, sistema: {self.sistema}'


