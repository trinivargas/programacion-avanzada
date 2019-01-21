from collections import namedtuple, defaultdict, deque

"""
Aquí están las estructuras de datos para guardar la información respectiva.

NO MODIFICAR.
"""

# Como se vio en la ayudantía, hay varias formas de declarar una namedtuple :)
Entrenador = namedtuple('Entrenador', 'nombre apellido')
Pokemon = namedtuple('Pokemon', ['nombre', 'tipo', 'max_solicitudes'])
Solicitud = namedtuple('Solicitud', ['id_entrenador', 'id_pokemon'])

################################################################################
"""
En esta sección debe completar las funciones para cargar los archivos al sistema.

Puedes crear funcionas auxiliar si tú quieres, ¡pero estas funciones DEBEN
retornar lo pedido en el enunciado!
"""

def cargar_entrenadores(ruta_archivo):
    """
    Esta función debería leer el archivo archivo_entrenadores y cargarlo usando
    las estructuras entregadas.
    """
    entrenadores = dict()
    with open(ruta_archivo, 'r', encoding='latin-1') as archivo: #el with lo copie de la ayudantia
        for linea in archivo:
            id_entrenador, nombre, apellido = linea.split(';')
            entrenadores[id_entrenador] = Entrenador(nombre, apellido)
    return entrenadores


def cargar_pokemones(ruta_archivo):
    """
    Esta función debería leer el archivo archivo_pokemones y cargarlo usando las
    estructuras entregadas.
    """
    pokemones = dict()
    with open(ruta_archivo, 'r', encoding='latin-1') as archivo:  # el with lo copie de la ayudantia
        for linea in archivo:
            id_pokemon, nombre, tipo, max_solicitudes = linea.split(';')
            entrenadores[id_pokemon] = Pokemon(nombre, tipo, max_solicitudes)
    return pokemones


def cargar_solicitudes(ruta_archivo):
    """
    Esta función debería leer el archivo archivo_solicitudes y cargarlo usando
    las estructuras entregadas. Creo que hay que usar deque
    """
    solicitudes = deque()
    with open(ruta_archivo, 'r', encoding='latin-1') as archivo:  # el with lo copie de la ayudantia
        for linea in archivo:
            id_entrenador, id_pokemon = linea.split(';')
            solicitud = Solicitud(id_entrenador, id_pokemon)
            solicitudes.append(solicitud)
    return solicitudes

################################################################################

"""
Lógica del Sistema.
Debes completar esta función como se dice en el enunciado.
"""

def sistema(modo, entrenadores, pokemones, solicitudes):
    """
    Esta función se encarga de llevar a cabo la 'simulación', de acuerdo al modo
    entregado.
    """
    duenos = dict()
    for entrenador in entrenadores.keys():
        duenos[entrenador] = set()
    if modo == '1':
        while len(solicitudes) > 0:
            solicitud = solicitudes.popleft()
            id_entrenador = solicitud.id_entrenador
            id_pokemon = solicitud.id_pokemon
            pokemon = pokemones[id_pokemon]
            if pokemon.max_solicitudes == 1:
                # asignar pokemon al entrenador buscar duenos set del entrenador
                pokemones_del_dueno = duenos[id_entrenador] # es un set
                pokemones_del_dueno.add(pokemon)
                pokemon.max_solicitudes += -1
            elif pokemon.max_solicitudes > 1:
                pokemon.max_solicitudes += -1


    elif modo == '2':
        pass

    return duenos # tiene que retornar

################################################################################
"""
Funciones de consultas, deben rellenarlos como dice en el enunciado :D.
"""

def pokemones_por_entrenador(id_entrenador, resultado_simulacion):
    """
    Esta función debe retornar todos los pokemones que ganó el entrenador con el
    id entregado.

    Recuerda que esta función debe retornar una lista.
    """
    return list(duenos[id_entrenador])

def mismos_pokemones(id_entrenador1, id_entrenador2, resultado_simulacion):
    """
    Esta función debe retornar todos los pokemones que ganó tanto el entrenador
    con el id_entrenador1 como el entrenador con el id_entrenador2.

    Recuerda que esta función debe retornar una lista.
    """
    pass

def diferentes_pokemones(id_entrenador1, id_entrenador2, resultado_simulacion):
    """
    Esta función debe retornar todos los pokemones que ganó el entrenador con
    id_entrenador1 y que no ganó el entrenador con id_entrenador2.

    Recuerda que esta función debe retornar una lista.
    """
    pass


if __name__ == '__main__':

    ############################################################################
    """
    Poblando el sistema.
    Ya se hacen los llamados a las funciones, puedes imprimirlos para ver si se
    cargaron bien.
    """

    entrenadores = cargar_entrenadores('entrenadores.txt') # tengo que retornar el diccionario
    pokemones = cargar_pokemones('pokemones.txt')
    solicitudes = cargar_solicitudes('solicitudes.txt')

    print(entrenadores)
    print(pokemones)
    print(solicitudes)

    ################################   MENU   ##################################
    """
    Menú.
    ¡No debes cambiar nada! Simplemente nota que es un menú que pide input del
    usuario, y en el caso en que este responda con "1" ó "2", entonces se hace
    el llamado a la función. En otro caso, el programa termina.
    """

    eleccion = input('Ingrese el modo de lectura de solicitudes:\n'
                 '1: Orden de llegada\n'
                 '2: Orden Inverso de llegada\n'
                 '>\t')

    if eleccion in {"1", "2"}:
        resultados_simulacion = sistema(eleccion, entrenadores,
                                        pokemones, solicitudes)
    else:
        exit()

    ##############################   Pruebas   #################################
    """
    Casos de uso.

    Aquí pueden probar si sus consultas funcionan correctamente.
    """
