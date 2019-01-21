class Nodo:
    def __init__(self, id_, entidad, distancia=None):
        self.id_ = id_
        self.distancia = distancia
        self.entidad = entidad
        self.siguiente = None


class ListaLigada:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar(self, id_, valor=None, distancia=None):
        nuevo = Nodo(id_, valor, distancia)
        if not self.cabeza:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo

    def __getitem__(self, id_):
        nodo_actual = self.cabeza
        while nodo_actual is not None:
            if nodo_actual.id_ == id_:
                return nodo_actual.entidad
            nodo_actual = nodo_actual.siguiente
        return None

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual
            actual = actual.siguiente

    def eliminar(self, id_):
        if self.cabeza.id_ == id:
            self.cabeza = self.cabeza.siguiente
            return
        anterior = self.cabeza
        actual = self.cabeza.siguiente
        while actual is not None:
            if actual.id_ == id_:
                anterior.siguiente = actual.siguiente
                return actual
            anterior = actual
            actual = actual.siguiente

    def __bool__(self):
        if self.cabeza is None:
            return False
        return True

    def popleft(self):
        cabeza = self.cabeza
        if self.cabeza is not None:
            self.cabeza = self.cabeza.siguiente
            return cabeza.entidad

    def en(self, id_):
        actual = self.cabeza
        while actual is not None:
            if actual.id_ == id_:
                return True
            actual = actual.siguiente
        return False

class NodoConexion:
    def __init__(self, tipo1, entidad1, tipo2, entidad2, distancia):
        self.tipo1 = tipo1
        self.nodo1 = entidad1
        self.tipo2 = tipo2
        self.nodo2 = entidad2
        self.distancia = distancia
        self.siguiente = None


class Conexiones:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.conexiones = ListaLigada()

    def agregar(self, tipo1, entidad1, tipo2, entidad2, distancia):
        nuevo = NodoConexion(tipo1, entidad1, tipo2, entidad2, distancia)
        if not self.cabeza:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual
            actual = actual.siguiente
