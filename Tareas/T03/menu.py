from estructuras import ListaLigada
from errores import InvalidQuery, ForbidenAction, ElectricalOverload
from entidades import Casa, Distribucion, Transmision, Elevadora, Central
from crear_nodos import CreacionNodos
from crear_arista import ConectarNodos
from eliminar_arista import EliminarArista
from consultas import Consultas
from eliminar_nodo import EliminarNodo
ρ = 0.0172

class Menu:
    def __init__(self, red):
        self.red = red
        self._crear_nodos = CreacionNodos(self, self.red)
        self._crear_aristas = ConectarNodos(self, self.red)
        self._consultas = Consultas(self, self.red)
        self._eliminar_nodo = EliminarNodo(self, self.red)
        self._eliminar_arista = EliminarArista(self, self.red)

    def menu_principal(self):
        opcion = '-1'
        while opcion != '0':
            print('\nSeleccione una opción:\n(1) Consultas\n'
                  '(2) Agregar Nodo\n(3) Remover Nodo\n(4) Agregar Arista\n'
                  '(5) Remover Arista\n(0) Salir')
            opcion = self.opcion(0, 5)
            if opcion == '1':
                self._consultas.menu()
            elif opcion == '2':
                self._crear_nodos.menu()
            elif opcion == '3':
                self._eliminar_nodo.menu()
            elif opcion == '4':
                self._crear_aristas.menu()
            elif opcion == '5':
                self._eliminar_arista.menu()

    def opcion(self, inicio, fin):
        try:
            o = self._opcion(inicio, fin)
        except InvalidQuery as err:
            print(err, 'Opción inválida')
            o = self.opcion(inicio, fin)
        return o

    def _opcion(self, inicio, fin):
        opcion = input('Opción: ')
        if not opcion.isdigit() or not inicio <= int(opcion) <= fin:
            raise InvalidQuery()
        return opcion

    def confirmar_cambios(self):
        try:
            r = self._pedir_confirmacion()
        except InvalidQuery as err:
            print(err, 'No ingresó una respuesta válida.')
            r = self.confirmar_cambios()
        return r

    def _pedir_confirmacion(self):
        print('¿Quiere realizar los cambios?')
        opcion = input('[y/n] ')
        if opcion == 'y' or opcion == 'n':
            return opcion
        raise InvalidQuery('')

    def pedir_nodo(self):
        try:
            nodo = self._pedir_nodo()
        except InvalidQuery as err:
            if 'opcion' in str(err):
                print(err, 'No ingresó una opción válida')
            else:
                print(err, 'No existe ese nodo')
            nodo = self.pedir_nodo()
        return nodo

    def _pedir_nodo(self):
        print('Ingrese el tipo de nodo\n(1) Casa\n(2)'
              ' Distribución\n(3) Transmision\n(4) Elevadora\n(5) Central')
        opcion = input('Opción: ')
        if not opcion.isdigit() or not 0 < int(opcion) < 6:
            raise InvalidQuery('opcion')
        id_ = input('id del nodo: ')
        if not id_.isdigit():
            raise InvalidQuery('id')
        nodo = None
        if opcion == '1':
            nodo = self.red.casas[id_]
        elif opcion == '2':
            nodo = self.red.distribuciones[id_]
        elif opcion == '3':
            nodo = self.red.transmisiones[id_]
        elif opcion == '4':
            nodo = self.red.elevadoras[id_]
        elif opcion == '5':
            nodo = self.red.centrales[id_]
        if nodo is None:
            raise InvalidQuery('None')
        return nodo

