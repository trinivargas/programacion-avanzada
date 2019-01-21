from errores import InvalidQuery, ForbidenAction, ElectricalOverload
from entidades import Central, Elevadora, Transmision, Distribucion, Casa
from estructuras import Conexiones


class EliminarArista:
    def __init__(self, principal, red):
        self.principal = principal
        self.red = red
        self.conexiones = Conexiones()

    def menu(self):
        self.conexiones = Conexiones()
        self._menu_1()

    def _menu_1(self):
        try:
            self._menu_2()
        except InvalidQuery as err:
            print(err)
            self._menu_1()
        except ElectricalOverload as err:
            print(f'{err}: La acción agregar_nodo sobrecarga la red a '
                  f'{err.potencia} kW')
            self._menu_1()
        except ForbidenAction as err:
            print(err)
            self._menu_1()

    def _menu_2(self):
        self.desconectar_nodos()
        opcion = '-1'
        while opcion != '0':
            print('\nOpciones:\n(1) Eliminar Arista\n(0) Volver')
            opcion = self.principal.opcion(0, 1)
            if opcion == '1':
                self.desconectar_nodos()
        self.confirmar_cambios()

    def confirmar_cambios(self):
        if not self._confirmar_cambios():
            for conexion in self.conexiones:
                self.conectar_nodos(conexion)

    def _confirmar_cambios(self):
        try:
            self.red.potencia_real_red()
        except ElectricalOverload as err:
            print(f'{err}: La acción agregar_nodo sobrecarga la red a '
                  f'{err.potencia} kW')
        except InvalidQuery as err:
            print(err)
        except ForbidenAction as err:
            print(err)
        else:
            r = self.principal.confirmar_cambios()
            if r == 'y':
                return True
        return False

    def _desconectar_nodos_1(self):
        print('Ingrese los nodos que quiere desconectar\nNodo 1:')
        nodo1 = self.principal.pedir_nodo()
        print('Nodo 2: ')
        nodo2 = self.principal.pedir_nodo()
        return self._desconectar_nodos_2(nodo1, nodo2)

    def desconectar_nodos(self):
        try:
            c = self._desconectar_nodos_1()
        except ForbidenAction as err:
            print(err, f'Accion {err.accion} invalida {err.razon}')
            c = self.desconectar_nodos()
        return c

    def _desconectar_nodos_2(self, nodo1, nodo2):
        if isinstance(nodo1, Central) and isinstance(nodo2, Elevadora):
            self.desconectar_elevadora_central(nodo2, nodo1)
        elif isinstance(nodo2, Central) and isinstance(nodo1, Elevadora):
            self.desconectar_elevadora_central(nodo1, nodo2)
        elif isinstance(nodo1, Elevadora) and isinstance(nodo2, Transmision):
             self.desconectar_elevadora_transmision(nodo1, nodo2)
        elif isinstance(nodo2, Elevadora) and isinstance(nodo1, Transmision):
            self.desconectar_elevadora_transmision(nodo2, nodo1)
        elif isinstance(nodo1, Transmision) and isinstance(nodo2, Distribucion):
            self.desconectar_transmision_distribucion(nodo1, nodo2)
        elif isinstance(nodo2, Transmision) and isinstance(nodo1, Distribucion):
            self.desconectar_transmision_distribucion(nodo2, nodo1)
        elif isinstance(nodo1, Distribucion) and isinstance(nodo2, Casa):
            self.desconectar_distribucion_casa(nodo1, nodo2)
        elif isinstance(nodo2, Distribucion) and isinstance(nodo1, Casa):
            self.desconectar_distribucion_casa(nodo2, nodo1)
        elif isinstance(nodo1, Casa) and isinstance(nodo2, Casa):
            self.desconectar_casa_casa(nodo1, nodo2)
        else:
            raise ForbidenAction('', 'eliminar_conexion',f'entre {nodo1.nombre}'
                                                         f' y {nodo2.nombre}')

    def desconectar_elevadora_central(self, elevadora, central):
        for central_elevadora in elevadora.centrales:
            if central_elevadora.id_ == central.id_:
                dist = central_elevadora.distancia
                elevadora.eliminar_conexion_central(central.id_)
                self.conexiones.agregar('', elevadora, '', central, dist)

    def desconectar_elevadora_transmision(self, elevadora, transmision):
        for transmision_elevadora in elevadora.conexiones:
            if transmision_elevadora.id_ == transmision.id_:
                dist = transmision_elevadora.distancia
                elevadora.eliminar_conexion(transmision.id_)
                self.conexiones.agregar('', elevadora, '', transmision, dist)

    def desconectar_transmision_distribucion(self, transmision, distribucion):
        for distribucion_trans in transmision.conexiones:
            if distribucion_trans.id_ == distribucion.id_:
                dist = distribucion_trans.distancia
                transmision.eliminar_conexion(distribucion.id_)
                self.conexiones.agregar('', transmision, '', distribucion, dist)

    def desconectar_distribucion_casa(self, distribucion, casa):
        for casa_dist in distribucion.conexiones:
            if casa_dist.id_ == casa.id_:
                dist = casa_dist.distancia
                distribucion.eliminar_conexion(casa.id_)
                self.conexiones.agregar('', distribucion, '', casa, dist)

    def desconectar_casa_casa(self, casa1, casa2):
        if casa1.conexiones.en(casa2.id_):
            for casa_c in casa1.conexiones:
                if casa_c.id_ == casa2.id_:
                    dist = casa_c.distancia
                    casa1.eliminar_conexion(casa2.id_)
                    casa2.conectado -= 1
                    self.conexiones.agregar('', casa1, '', casa2, dist)
        elif casa2.conexiones.en(casa1.id_):
            for casa_c in casa2.conexiones:
                if casa_c.id_ == casa1.id_:
                    dist = casa_c.distancia
                    casa2.eliminar_conexion(casa1.id_)
                    casa1.conectado -= 1
                    self.conexiones.agregar('', casa2, '', casa1, dist)

    def conectar_nodos(self, conexion):
        if isinstance(conexion.nodo2, Central):
            return self.conectar_central(conexion)
        self.conectar_otros_nodos(conexion)

    def conectar_central(self, conexion):
        conexion.nodo1.conectar_central(conexion.nodo2, conexion.distancia)

    def conectar_otros_nodos(self, conexion):
        conexion.nodo1.agregar_conexion(conexion.nodo2, conexion.distancia)

    def pedir_distancia(self):
        try:
            dist = self._pedir_distancia()
        except InvalidQuery:
            print('Número ingresado es inválido')
            dist = self.pedir_distancia()
        return dist

    def _pedir_distancia(self):
        distancia = input('Distancia entre los nodos: ')
        if not distancia.replace('.', '').isdigit() or distancia.count('.') > 1:
            raise InvalidQuery('')
        return float(distancia)