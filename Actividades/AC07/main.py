


class Terreno:

    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = set()

    def conectar(self, terreno):
        self.conexiones.add(terreno.nombre)

    def desconectar(self, terreno):
        self.conexiones.remove(terreno.nombre)



class Ciudad:

    def __init__(self, path):
        self._terrenos = dict() # se guardan los nombres de los terrenos, no las instancias
        self.cargar_archivo(path)


    def cargar_archivo(self, path):
        with open(path, 'r') as file:
            for line in file:
                origen, destinos = line.strip().split(':')
                destinos = destinos.split(',')
                for destino in destinos:
                    self.agregar_calle(origen.strip(), destino.strip())

    def _crear_terreno(self, nombre_terreno): # también retorna el nodo si este ya existe
        terreno = self._terrenos.get(nombre_terreno)
        if terreno is None:
            terreno = Terreno(nombre_terreno)
            self._terrenos[nombre_terreno] = terreno
        return terreno


    def agregar_calle(self, origen, destino):
        terreno_origen = self._crear_terreno(origen)
        terreno_destino = self._crear_terreno(destino)
        terreno_origen.conectar(terreno_destino)


    def eliminar_calle(self, origen, destino): # elimina solo en el sentido dado
        terreno_origen = self._crear_terreno(origen)
        terreno_destino = self._crear_terreno(destino)
        terreno_origen.desconectar(terreno_destino)

    @property
    def terrenos(self):
        return {terreno for terreno in self._terrenos}

    @property
    def calles(self):
        calles = set()
        for terreno in self._terrenos.values():
            for destino in terreno.conexiones:
                calles.add((terreno.nombre, destino))
        return calles


    def verificar_ruta(self, ruta):
        # si la lista es vacía
        if not ruta:
            return True
        terreno_origen = self._terrenos.get(ruta[0])
        if terreno_origen is None:
            return False
        if len(ruta) == 1:
            return True
        # existe la conexion
        if ruta[1] not in terreno_origen.conexiones:
            return False
        return self.verificar_ruta(ruta[1:])


    def entregar_ruta(self, origen, destino):
        ruta = self._entregar_ruta(origen, destino)
        for i, terreno in enumerate(ruta):
            ruta[i] = terreno.nombre
        return ruta

    def _entregar_ruta(self, origen, destino):
        if origen == destino:
            return True
        origen = self._terrenos.get(origen)
        destino = self._terrenos.get(destino)
        if origen is None or destino is None:
            return None
        cola = [[origen]]
        visited = list()
        while len(cola):
            current_path = cola.pop(0)
            current = current_path[-1]
            if current not in visited:
                lista_vecinos = [self._terrenos.get(x) for x in current.conexiones]
                for vecino in lista_vecinos:
                    cola.append(list(current_path) + [vecino])
                    if vecino == destino:
                        return cola[-1]
                visited.append(current)
        return list()


    def ruta_corta(self, origen, destino):
        return self.entregar_ruta(origen, destino)


    def ruta_entre_bombas(self, origen, *destinos):
        pass

    def ruta_corta_entre_bombas(self, origen, *destinos):
        pass




if __name__ == '__main__':
    ciudad_facil = Ciudad('facil.txt')
    ciudad_media = Ciudad('medio.txt')
    ciudad_dificil = Ciudad('dificil.txt')
    ciudad_kratos = Ciudad('kratos.txt')

    #ciudad_dificil.eliminar_calle('D', 'G')
    #ciudad_facil.agregar_calle('A', 'F')
    print(ciudad_facil.verificar_ruta(['A', 'C', 'E', 'F']))

    print('Terrenos ciudad facil.txt', ciudad_facil.terrenos)
    print('Calles ciudad facil', ciudad_facil.calles)
    


    print('Ruta entre A y F de la ciudad facil.txt',
          ciudad_facil.entregar_ruta('A', 'F'))
    print('Ruta entre A y D de la ciudad medio.txt',
          ciudad_media.entregar_ruta('A', 'D'))
    print('Ruta entre A y M de la ciudad dificil  ',
          ciudad_dificil.entregar_ruta('A', 'M'))
    print('Ruta entre A y N de la ciudad kratos.txt',
          ciudad_kratos.entregar_ruta('A', 'N'))
    # Listo!!!
