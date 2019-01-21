from estructuras import Conexiones, ListaLigada
from errores import ElectricalOverload
from entidades import Central, Elevadora, Transmision, Distribucion, Casa

class EliminarNodo:
    def __init__(self, principal, red):
        self.principal = principal
        self.red = red
        self.elevadora_desconectada = ListaLigada()

    def menu(self):
        try:
            self._menu()
        except:
            print('Error')
            self.menu()

    def _menu(self):
        opcion = '-1'
        todos_cambios = ListaLigada()
        while opcion != '0':
            print('(1) Eliminar nodo\n(0) Confirmar cambios y Salir')
            opcion = self.principal.opcion(0, 1)
            if opcion == '1':
                conexiones = self.eliminar_nodo()
                todos_cambios.agregar(0, conexiones)
        self.confirmar_cambios(todos_cambios)

    def confirmar_cambios(self, lista_ligada_cambios):
        r = self.realizar_cambios()
        if r is None or r == 'n':
            self.rehacer_cambios(lista_ligada_cambios)
        elif r == 'y':
            self.desconectar_elevadoras()

    def desconectar_elevadoras(self):
        for elevadora in self.elevadora_desconectada:
            elevadora.entidad.eliminar_conexiones()

    def rehacer_cambios(self, lista_cambios):
        for lista_conexiones in lista_cambios: # conexiones es un nodo de lista ligada id_ = 0
            for conexion in lista_conexiones.entidad:
                if conexion.tipo1 == 'central' or conexion.tipo2 == 'central':
                    self._conectar_central(conexion.nodo1, conexion.nodo2,
                                           conexion.distancia)
                else:
                    self._conectar_nodos(conexion.nodo1, conexion.nodo2,
                                         conexion.distancia)

    def realizar_cambios(self):
        try:
            self.red.potencia_real_red()
        except ElectricalOverload as err:
            print(f'{err}: La acción agregar_nodo sobrecarga la red a '
                  f'{err.potencia} kW')
            print(err, '\nNo se pueden realizar los cambios :(')
            return None
        return self.principal.confirmar_cambios()

    def eliminar_nodo(self):
        nodo = self.principal.pedir_nodo()
        sistema = self.red.encontrar_sistema(nodo.sistema)
        conexiones = Conexiones() # agregar!!!
        if isinstance(nodo, Casa):
            padres = self.encontrar_nodos_padre(nodo, sistema.distribuciones,
                                                sistema.casas)
            conexiones = self.eliminar_casa(nodo, padres)

        elif isinstance(nodo, Distribucion):
            padres = self.encontrar_nodos_padre(nodo, sistema.transmisiones)

        elif isinstance(nodo, Transmision):
            padres = self.encontrar_nodos_padre(nodo, sistema.elevadoras)

        elif isinstance(nodo, Central):
            conexiones = self.eliminar_central(nodo)

        elif isinstance(nodo, Elevadora):
            self.elevadora_desconectada.agregar(nodo)
            conexiones = self.eliminar_elevadora(nodo)
            #nodo.eliminar_conexiones()  al confirmar !!!
        return conexiones

    def encontrar_nodos_padre(self, nodo, posibles1, posibles2=None):
        padres = ListaLigada()
        for posible in posibles1:
            if posible.entidad.conexiones[nodo.id_] is not None:
                padres.agregar(posible.id_, posible.entidad)
        if posibles2 is not None:
            for posible in posibles2:
                if posible.entidad.conexiones[nodo.id_] is not None:
                    padres.agregar(posible.id_, posible.entidad)
        return padres

    def eliminar_elevadora(self, elevadora):
        conexiones = Conexiones()
        for central in elevadora.centrales:
            conexiones.agregar('elevadora', elevadora, 'central',
                               central.entidad, central.distancia)
            central.entidad.n_elevadoras -= 1
        return conexiones

    def eliminar_central(self, central):
        conexiones = Conexiones()
        sistema = self.red.encontrar_sistema(central.sistema)
        for elevadora in sistema.elevadoras:
            for central_elevadora in elevadora.entidad.centrales:
                if central_elevadora.id_ == central.id_:
                    c = central_elevadora.entidad
                    elevadora.entidad.eliminar_conexion_central(central.id_)
                    conexiones.agregar('elevadora', elevadora.entidad, 'central'
                                       , central, central_elevadora.distancia)
                    central.n_elevadoras -= 1
        return conexiones

    def _conectar_nodos(self, nodo1, nodo2, distancia): # no incluye centrales
        try:
            nodo2.agregar_conexion(nodo1, distancia)
        except ForbidenAction:
            nodo1.agregar_conexion(nodo2, distancia)

    def _conectar_central(self, nodo1, nodo2, distancia):
        if isinstance(nodo1, Central):
            nodo2.conectar_central(nodo1, distancia)
            nodo1.n_elevadoras += 1
        else:
            nodo1.conectar_central(nodo2, distancia)
            nodo2.n_elevadoras += 1

    def eliminar_casa(self, nodo1, nodos_padre):
        conexiones = Conexiones()
        for nodo in nodos_padre:
            for conexion in nodo.entidad.conexiones:
                if conexion.id_ == nodo1.id_:
                    conexiones.agregar('casa', nodo1, 'casa', conexion.entidad,
                                       conexion.distancia)
            nodo.entidad.eliminar_conexion(nodo1.id_)
            nodo.conectado -= 1
        return conexiones

