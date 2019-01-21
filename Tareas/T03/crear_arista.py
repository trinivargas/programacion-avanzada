from errores import InvalidQuery, ForbidenAction, ElectricalOverload
from entidades import Central, Elevadora, Transmision, Distribucion, Casa
from estructuras import Conexiones


class ConectarNodos:
    def __init__(self, principal, red):
        self.principal = principal
        self.red = red

    def menu(self):
        try:
            self._menu()
        except InvalidQuery as err:
            print(err, 'input inválido')
            self.menu()
        except ForbidenAction as err:
            print(err, 'accion nó valida')
            self.menu()
        except ElectricalOverload as err:
            print(f'{err}: La acción agregar_nodo sobrecarga la red a '
                  f'{err.potencia} kW')
            self.menu()

    def _menu(self):
        self.conectar_nodos()
        opcion = '-1'
        while opcion != '0':
            print('\nOpciones:\n(1) Crear Arista\n(0) Volver')
            opcion = self.principal.opcion(0, 1)
            if opcion == '1':
                self.conectar_nodos()

    def conectar_nodos(self):
        print('Ingrese los nodos que quiere conectar\nNodo 1:')
        nodo1 = self.principal.pedir_nodo()
        print('Nodo 2: ')
        nodo2 = self.principal.pedir_nodo()
        if isinstance(nodo1, Central) or isinstance(nodo2, Central):
            return self.conectar_central(nodo1, nodo2)
        else:
            n_padre = self._conectar_nodos(nodo1, nodo2)
        if n_padre is None:
            print('No se puede realizar la conexion :(')
        else:
            if n_padre == 'nodo1':
                self.confirmar_conexion(nodo1, nodo2)
            else:
                self.confirmar_conexion(nodo2, nodo1)

    def _conectar_nodos(self, nodo1, nodo2):
        distancia = self.pedir_distancia()
        n_padre = None
        try:
            nodo2.agregar_conexion(nodo1, distancia)
            self.red.potencia_real_red()
        except ForbidenAction:
            try:
                nodo1.agregar_conexion(nodo2, distancia)
                self.red.potencia_real_red()
            except ForbidenAction as err:
                print(err)
            except ElectricalOverload as err:
                print(f'{err}: La acción agregar_nodo sobrecarga la red a '
                      f'{err.potencia} kW')
                nodo1.eliminar_conexion(nodo2.id_)
            else:
                n_padre = 'nodo1'
        except ElectricalOverload as err:
            print(f'{err}: La acción agregar_nodo sobrecarga la red a '
                  f'{err.potencia} kW')
            nodo2.eliminar_conexion(nodo1.id_)
        else:
            n_padre = 'nodo2'
        return n_padre

    def conectar_central(self, nodo1, nodo2):
        elevadora = self._conectar_central(nodo1, nodo2)
        if elevadora is None:
            print('No se puede realizar la conexion :(')
            return
        if elevadora == 'nodo1':
            padre = nodo1
            hijo = nodo2
        else:
            padre = nodo2
            hijo = nodo1
        r = self.confirmar_conexion(padre, hijo)
        if r == 'n':
            if elevadora == 'nodo1':
                nodo1.eliminar_conexion_central(nodo2.id_)
            else:
                nodo2.eliminar_conexion_central(nodo1.id_)

    def _conectar_central(self, nodo1, nodo2):
        distancia = self.pedir_distancia()
        elevadora = None
        try:
            if isinstance(nodo1, Elevadora):
                nodo1.conectar_central(nodo2, distancia)
        except InvalidQuery as err1:
            try:
                if isinstance(nodo2, Elevadora):
                    nodo2.conectar_central(nodo1, distancia)
            except InvalidQuery as err2:
                print(err2)
            else:
                elevadora = 'nodo2'
        else:
            elevadora = 'nodo1'
        return elevadora

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

    def confirmar_conexion(self, padre, hijo):
        r = self.principal.confirmar_cambios()
        if r == 'n':
            padre.eliminar_conexion(hijo.id_)


