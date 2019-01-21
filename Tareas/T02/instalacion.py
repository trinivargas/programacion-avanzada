from collections import deque
from abc import ABC, abstractmethod #from itertools import count ## FALTA


class Instalacion(ABC): ##
    #   _id = count(start=0)
    def __init__(self, cap_max, costo):
        super().__init__() #self._id = next(Instalacion._id)
        self.capacidad_maxima = cap_max
        self.costo = costo
        self.ganancias = 0
        self.n_clientes = 0
        self.tiempo_cerrado = 0
        self.personal = set()
        self.fila_espera = deque()
        self.clientes_instalacion = set()
        self.clientes_llegando = set()
        self.cerrado = False

    @abstractmethod
    def funcionando(self):
        pass

    @abstractmethod
    def duracion_por_persona(self, cliente):
        pass

    @abstractmethod
    def asistir(self, cliente):
        pass

    def destino(self):
        pass

    def coordenadas_adentro(self):
        pass

    def permitir_ingreso(self, cliente):
        if cliente.dinero >= self.costo:
            return True
        return False

    def cobrar(self, cliente):
        cliente.dinero -= self.costo
        self.ganancias += self.costo

    def llega_cliente(self, cliente):
        if self.funcionando and self.permitir_ingreso(cliente):
            self.clientes_llegando.add(cliente)
            cliente.destino = self.destino
            cliente.actividad = 'Instalacion o juego'

    def llega_trabajador(self, trabajador):
        trabajador.trabajar()
        self.personal.add(trabajador)

    def tick_clientes(self):
        if self.funcionando and not self.cerrado:
            # se agrega a la lista de espra los clientes que llegaron
            clientes_llegaron = set()
            for cliente in self.clientes_llegando:
                if (cliente.x, cliente.y) == self.destino:
                    clientes_llegaron.add(cliente)
                    self.fila_espera.append(cliente)
            for cliente in clientes_llegaron:
                self.clientes_llegando.remove(cliente)

            # si hay espacio entran los clientes y se le asigna el tiempo
            while len(self.clientes_instalacion) < self.capacidad_maxima \
                    and self.fila_espera:
                nuevo = self.fila_espera.popleft()
                nuevo.tiempo_restante_actividad = self.duracion_por_persona(nuevo)
                nuevo.destino = self.coordenadas_adentro
                self.clientes_instalacion.add(nuevo)

            # disminuir en un minuto el tiempo restante de los clientes
            clientes_desocupados = set()
            for cliente in self.clientes_instalacion:
                cliente.tiempo_restante_actividad -= 1
                if cliente.tiempo_restante_actividad <= 0:
                    clientes_desocupados.add(cliente)

            # realizar los cambios de atributos de los clientes, cobrar y
            # desocupar la instalación
            self._desocupar(clientes_desocupados)
            return

        # si la instalacion se cierra o está cerrada por falta de personal
        self.tiempo_cerrado += 1
        for cliente in self.fila_espera:
            cliente.desocupar()
            cliente.destino = self.destino
        for cliente in self.clientes_instalacion | self.clientes_llegando:
            cliente.desocupar()
            cliente.destino = self.destino

        self.fila_espera = deque()
        self.clientes_instalacion = set()
        self.clientes_llegando = set()

    def _desocupar(self, clientes_desocupados):
        for cliente in clientes_desocupados:
            self.n_clientes += 1
            self.clientes_instalacion.remove(cliente)
            self.asistir(cliente)
            cliente.desocupar()


    def tick_personal(self):
        personal_termina_turno = set()
        for trabajador in self.personal:
            trabajador.tiempo_restante_actividad -= 1
            if trabajador.tiempo_restante_actividad <= 0:
                personal_termina_turno.add(trabajador)

        for trabajador in personal_termina_turno:
            self.personal.remove(trabajador)

        # retorna los trabajadores que van a descansar
        return personal_termina_turno
