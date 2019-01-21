from collections import namedtuple
from functools import reduce

# NO MODIFICAR ESTA FUNCION
def foreach(function, iterable):
    for elem in iterable:
        function(elem)


# Named tuples para cada entidad
Ciudad = namedtuple("Ciudad", ["sigla_pais", "nombre"])
Pais = namedtuple("Pais", ["sigla", "nombre"])
Persona = namedtuple("Persona", [
    "nombre", "apellido", "edad", "sexo", "ciudad_residencia",
    "area_de_trabajo", "sueldo"
])

###########################


def leer_ciudades(ruta_archivo_ciudades):
    '''
    :param ruta_archivo_ciudades: str
    :return: generador
    '''
    with open(ruta_archivo_ciudades, 'r', encoding='utf-8') as file:
        for line in file:
            sigla_pais, nombre = line.strip().split(',')
            yield Ciudad(sigla_pais, nombre)


def leer_paises(ruta_archivo_paises):
    '''
    :param ruta_archivo_paises: str
    :return: generador
    '''
    with open(ruta_archivo_paises, 'r',encoding='utf-8') as file:
        for line in file:
            sigla, nombre = line.strip().split(',')
            yield Pais(sigla, nombre)


def leer_personas(ruta_archivo_personas):
    '''
    :param ruta_archivo_personas: str
    :return: generador
    '''
    with open(ruta_archivo_personas, 'r', encoding='utf-8') as file:
        for line in file:
            yield Persona(*line.strip().split(','))


def sigla_de_pais(nombre_pais, paises):
    '''
    :param nombre_pais: str
    :param paises: iterable de Paises (instancias)
    :return: sigla correspondiente al pais nombre_pais: str
    '''
    pais = list(filter(lambda pais: nombre_pais == pais.nombre, paises))
    return pais[0].sigla


def ciudades_por_pais(nombre_pais, paises, ciudades):
    '''
    :param nombre_pais: str
    :param paises: iterable de Paises (instancias)
    :param ciudades: iterable de Ciudades (instancias)
    :return: generador
    '''
    # Retorna las ciudades pertenecientes al pais
    sigla_pais = sigla_de_pais(nombre_pais, paises)
    return filter(lambda ciudad: ciudad.sigla_pais == sigla_pais, ciudades)
    #for ciudad in ciudades_pais:
    #    yield ciudad

def personas_por_pais(nombre_pais, paises, ciudades, personas):
    '''
    :param nombre_pais: str
    :param paises: iterable de Paises (instancias)
    :param ciudades: iterable de Ciudades (instancias)
    :param personas: iterable de Personas (instancias)
    :return: generador
    '''
    # retorna generador personas, ciudad de residencia es el nombre
    ciudades = ciudades_por_pais(nombre_pais, paises, ciudades)
    # para cada persona si la ciudad esta en ciudades
    # ciudades retorna la namedtuple
    nombres_ciudades = list(map(lambda ciudad: ciudad.nombre, ciudades))
    return filter(lambda persona: persona.ciudad_residencia in nombres_ciudades ,personas)



def sueldo_promedio(personas):
    '''
    :param personas: iterable de Personas (lista de instancias)
    :return: promedio (int o float)
    '''
    sueldos = list(map(lambda persona: float(persona.sueldo), personas))
    return reduce(lambda x, y: x + y, sueldos) / len(sueldos)


def cant_personas_por_area_de_trabajo(personas):
    '''
    :param personas: iterable de Personas (lista de instancias)
    :return: dict {area_de_trabajo: int}
    '''
    areas_trabajo = {persona.area_de_trabajo: 0 for persona in personas}
    #map(lambda persona: areas_trabajo[persona.area_de_trabajo] = 1, personas)
    return areas_trabajo

if __name__ == '__main__':
    RUTA_PAISES = "Paises.txt"
    RUTA_CIUDADES = "Ciudades.txt"
    RUTA_PERSONAS = "Personas.txt"

    # (1) Ciudades en Chile
    ciudades_chile = ciudades_por_pais('Chile', leer_paises(RUTA_PAISES),
                                       leer_ciudades(RUTA_CIUDADES))
    foreach(lambda ciudad: print(ciudad.sigla_pais, ciudad.nombre), ciudades_chile)

    # (2) Personas en Chile
    personas_chile = personas_por_pais('Chile', leer_paises(RUTA_PAISES),
                                       leer_ciudades(RUTA_CIUDADES),
                                       leer_personas(RUTA_PERSONAS))
    foreach(lambda p: print(p.nombre, p.ciudad_residencia), personas_chile)

    # (3) Sueldo promedio de personas del mundo
    sueldo_mundo = sueldo_promedio(leer_personas(RUTA_PERSONAS))
    # print('Sueldo promedio: ', sueldo_mundo)

    # (4) Cantidad de personas por profesion
    dicc = cant_personas_por_area_de_trabajo(leer_personas(RUTA_PERSONAS))
    foreach(lambda elem: print(f"{elem[0]}: {elem[1]}"), dicc.items())
