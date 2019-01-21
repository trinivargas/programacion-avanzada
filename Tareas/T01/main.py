from collections import namedtuple, Counterfrom datetime import datetimefrom math import sin, cos, asin, radiansfrom itertools import teefrom os import listdir, getcwdfrom iic2233_utils import parse, foreachfrom types import GeneratorTypecarpeta = "large/"Person = namedtuple('Person', 'id_ name class_ age')Airport = namedtuple('Airport', 'icao type lat long iso_country')Flight = namedtuple('Flight', 'id_ a_from a_to date')Travel = namedtuple('Travel', 'flight_id passenger_id')def distance(lat1, long1, lat2, long2):    '''retorna la distancia entre dos aeropuertos en millas nauticas'''    lat1, long1, lat2, long2 = map(lambda x: float(x),                                   (lat1, long1, lat2, long2))    a = sin(radians((lat2 - lat1) / 2)) ** 2    b = sin(radians((long2 - long1) / 2)) ** 2    c = (a + cos(radians(lat1)) * (cos(radians(lat2))) * b) ** .5    return abs(2 * 3440 * asin((c)))def datetime_type(date):    '''    recibe un string de la forma A-M-D H:M:S    retorna la fecha en tipo datetime.datetime '''    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')def load_database(db_type):    ''' retorna un generador con las personas, vuelos, aeropuertos o viajes '''    direction = direction_file(db_type)    dato = {'Travels': Travel, 'Passengers': Person, 'Airports': Airport,            'Flights': Flight}    with open(direction, 'r', encoding='utf-8-sig') as file:        file.readline()        for line in file:            yield dato[db_type](*line.strip().split(','))def direction_file(db_type):    ''' retorna el path del archivo'''    file_name = db_type.lower()    if db_type == 'Travels':        file_name = 'flights-passengers2'    return 'data/' + carpeta + '/' + file_name + '.csv'def operators(operator):    ''' retorna una función con la operación buscada'''    operators = {'<': lambda x, y: x < y, '>': lambda x, y: x > y,                '==': lambda x, y: x == y, '!=': lambda x, y: x != y,                'AND': lambda x, y: x & y, 'OR': lambda x, y: x | y,                'XOR': lambda x, y: x ^ y, 'DIFF': lambda x, y: x - y}    return operators[operator]def filter_flights(flights, airports, attr, symbol, value):    '''    recibe generadores de vuelos y aeropuertos, un attr de date o distance,    una operación y un valor para comparar    retorna alos vuelos que cumplen la condición'''    flights = set(f for f in flights)    if attr == 'distance':        airports = {a.icao: a for a in airports}    for f in flights:        if attr == 'date' and operators(symbol)(datetime_type(f.date), value):            yield f        elif attr == 'distance':            d = flight_distance(airports, f)            if operators(symbol)(d, value):                yield fdef flight_distance(airports, flight):    '''    recibe un diccionario con los aeropuertos y un vuelo    retorna la distancia del vuelo '''    lat_1, long_1 = airports[flight.a_from].lat, airports[flight.a_from].long    lat_2, long_2 = airports[flight.a_to].lat, airports[flight.a_to].long    return distance(lat_1, long_1, lat_2, long_2)def filter_passengers(passengers, flights, travels, icao, start, end):    ''' retorna todos los pasajeros que tengan como destino el aeropuerto    con icao indicado entre las fechas dadas '''    flight_ids = flights_airport(flights, icao, start, end)    travels_airport = filter(lambda t: t.flight_id in flight_ids, travels)    passengers_id = {t.passenger_id for t in travels_airport}    return filter(lambda p: p.id_ in passengers_id, passengers)def flights_airport(flights, icao, start, end):    '''recibe los vuelos y un icao    retorna todos los id de vuelos que llegan al aeropuerto entre las fechas '''    flights = filter(lambda f: f.a_to == icao, flights)  # a_to    if isinstance(start, str) and isinstance(end, str):        start, end = map(lambda x: datetime_type(x), (start, end))    flights = filter(lambda f: start <= datetime_type(f.date) <= end, flights)    return {f.id_ for f in flights}def filter_passengers_by_age(passengers, age, lower=True):    '''con todos los pasajeros que tengan una edad menor al age entregado'''    if lower:        return filter(lambda p: int(p.age) < int(age), passengers)    return filter(lambda p: int(p.age) >= int(age), passengers)def filter_airport_by_country(airports, iso):    return filter(lambda a: a.iso_country == iso, airports)def filter_airports_by_distance(airports, icao, dist, lower=False):    airports = {a for a in airports}    origin = list(filter(lambda a: a.icao == icao, airports))[0]    lat1, long1 = float(origin.lat), float(origin.long)    airports.remove(origin)    if lower:        return filter(lambda a:                      distance(lat1, long1, a.lat, a.long) < dist, airports)    return filter(lambda a:                  distance(lat1, long1, a.lat, a.long) >= dist, airports)def favourite_airport(passengers, flights, travels):    '''retorna un diccionario con keys de los identificadores de los paajero    y value el código del aeropuerto al que tuvo como destino más veces'''    passengers = {p.id_: set() for p in passengers}    flights = {f.id_: f.a_to for f in flights}    _ = [passengers[t.passenger_id].add(flights[t.flight_id]) for t in travels]    return {p[0]: Counter(p[1]).most_common(1)[0][0] for p in            passengers.items()}def passenger_miles(passengers, airports, flights, travels):    ap = {a.icao: (a.lat, a.long) for a in airports}    f_distance = {f.id_: distance(*ap[f.a_from], *ap[f.a_to]) for f in flights}    passengers = {p.id_: [] for p in passengers}    _ = [passengers[t.passenger_id].append(f_distance[t.flight_id]) for t in         travels if t.passenger_id in passengers]    return {p[0]: sum(p[1]) for p in passengers.items()}def popular_airports(flights, airports, travels, topn, avg=False):    '''retorna los n aeropuertos con más pasajeros por vuelo o en total '''    airports = number_passengers_airports(airports, flights, travels)    if avg:        airports = {a[0]: sum(a[1]) / len(a[1]) for a in airports.items() if                    len(a[1]) != 0}    if not avg:        airports = {a[0]: sum(a[1]) for a in airports.items()}    return list(sorted(airports.keys(), key=lambda x: airports[x])[- topn:])def number_passengers_airports(airports, flights, travels):    ''' recibe aeropuertos, vuelos y viajes    retorna un diccionario con key icao del aeropuerto y value una lista    con el numero de pasajeros de cada vuelo que partió o llegó al aeropuerto'''    flights1, flights2 = tee(flights)    airports = {a.icao: [] for a in airports}    f_airports = {f.id_: (f.a_from, f.a_to) for f in flights1}    p_flights = {f.id_: [] for f in flights2}    _ = [p_flights[t.flight_id].append(1) for t in travels]    p_flights = {p[0]: sum(p[1]) for p in p_flights.items()}    _ = [airports[f_airports[p[0]][0]].append(p[1]) for p in p_flights.items()]    _ = [airports[f_airports[p[0]][1]].append(p[1]) for p in p_flights.items()]    return airportsdef airport_passengers(passengers, flights, travels, icao1, icao2, operation):    ''' retorna los pasajeros que cumplen la condicion de haber pasado    o no por los aeropuertos '''    flights = {f for f in flights}    travels = {t for t in travels}    passengers = {p for p in passengers}    passengers_1 = one_airport_passengers(flights, travels, passengers, icao1)    passengers_2 = one_airport_passengers(flights, travels, passengers, icao2)    return operators(operation)(passengers_1, passengers_2)def one_airport_passengers(flights, travels, passengers, icao):    ''' retorna todos los pasajeros que pasaron por el aeropuerto'''    f_icao = {f.id_ for f in flights if f.a_from == icao or f.a_to == icao}    p_id = {t.passenger_id for t in travels if t.flight_id in f_icao}    return {p for p in passengers if p.id_ in p_id}def furthest_distance(passengers, airports, flights, travels, icao, n=3):    '''retorna n pasajeros cuyo destino es el más lejano '''    flights1, flights2 = tee(flights, 2)    airports_dist = airports_distance(airports, flights1, icao)    flights = {f.id_: airports_dist[f.a_to] for f in flights2}    passengers = {p.id_: p for p in passengers}    p_miles = {p: [0] for p in passengers}    _ = [p_miles[t.passenger_id].append(flights[t.flight_id]) for t in travels]    p_miles = {p[0]: max(p[1]) for p in p_miles.items()}    p_ids = sorted(p_miles.keys(), key=lambda x: p_miles[x])[- n:]    return [passengers[x] for x in p_ids]def airports_distance(airports, flights, icao):    ''' retorna un diccionario con la distancia del aeropuerto de origen    a cada aeropuerto'''    destination_airports = {f.a_to for f in flights}    airports = {a.icao: a for a in airports if                a.icao in destination_airports or a.icao == icao}    ubication = airports[icao].lat, airports[icao].long    return {a.icao: distance(*ubication, a.lat, a.long)            for a in airports.values()}def consults_dictionary():    ''' retorna la función pedida con un string del nombre'''    c = {'load_database': load_database, 'filter_flights': filter_flights,         'filter_passengers': filter_passengers,         'filter_passengers_by_age': filter_passengers_by_age,         'filter_airports_by_country': filter_airport_by_country,         'filter_airports_by_distance': filter_airports_by_distance,         'favourite_airport': favourite_airport,         'passenger_miles': passenger_miles,         'popular_airports': popular_airports,         'airport_passengers': airport_passengers,         'furthest_distance': furthest_distance}    return cdef read_consult(consult):    ''' ejecuta la función que está en un diccionario'''    consult, data = tuple(consult.items())[0]    data = [read_consult(d) if isinstance(d, dict) else d for d in data]    return consults(consult)(*data)def consults(consult):    ''' Recive a string and return the function'''    c = consults_dictionary()    return c[consult]def open_file():    ''' abre un archivo de consultas'''    file_name = input('Nombre de archivo: ')    #file_name = 'queries.txt'    if not file_name in listdir(getcwd()):        print("This file doesn't exist")        return    with open(file_name, 'r', encoding='utf-8') as file:        return [line.strip() for line in file]def consults_results(lines):    ''' usuario selecciona consultas e    imprime los resultados de las consultas de un archivo'''    print('\nConsultas disponibles')    foreach( print, [f'({x + 1}) {c}' for x, c in enumerate(lines)])    print('Ingrese las consultas a abrir separadas por comas')    options = input('Opciones: ')    options = [int(x.strip()) for x in options.split(',') if x.strip().isdigit()               and 0 < int(x.strip()) <= len(lines)]    return [read_consult(parse(lines[x - 1])) for x in options]def new_consult_results(consults):    ''' retorna los resultados de las consultas ingresadas'''    if isinstance(parse(consults), list):        consults = [c for c in parse(consults)]        return [read_consult(c) for c in consults]    return [read_consult(parse(consults))]def open_file_consult_menu():    ''' menú para abrir un archivo de consultas'''    lines = open_file()    results = list(consults_results(lines))    foreach(print_result, results)    print('\n(1) Ver otra consulta\n(Otro) Salir')    opcion = input('Opción: ')    if opcion == '1':        open_file_consult_menu()def new_consult_menu():    ''' menú para ingresar nuevas consultas'''    print('Ingrese una consulta en el formato del enunciado')    consults = input('Consulta: ')    results = new_consult_results(consults)    foreach(print_result, results)    print('\n¿Guardar consulta?\n(1) Si\n(Otro) No')    opcion = input('Opción: ')    if opcion == '1':        save_consult(consults)    print('\n(1) Ingresar otra consulta\n(Otro) Salir')    opcion = input('Opción: ')    if opcion == '1':        new_consult_menu()def print_result(result):    ''' función que imprime los resultados de las consultas'''    if isinstance(result, (GeneratorType, filter)):        print(*result, sep=';')    elif isinstance(result, (dict, list, set)):        print(result)    else:        print(result)def string_result(result):    ''' función que retorna el resultado de una consulta como string para    guardar en un archivo'''    if isinstance(result, (GeneratorType, list, set, filter)):        return str(type(result)) + ',' + ';'.join([str(r) for r in result])    elif isinstance(result, dict):        return str(type(result)) + ',' + str(tuple(result.items()))[1:-1]def save_consult(consult):    ''' función que guarda las consultas en un archivo'''    with open('output.txt', 'a+', encoding='utf-8') as file:        pass    with open('output.txt', 'r+', encoding='utf-8') as file:        lines = len([1 for line in file])        _consult = consult        if isinstance(parse(consult), list):            _consult = ';'.join([str(c) for c in parse(consult)])        file.write(f'Consulta {lines//3 + 1}\n{_consult}\n')        results = [string_result(r) for r in new_consult_results(consult)]        file.write(';'.join(results) + '\n')def read_file_menu():    '''menú para abrir y editar el archivo output.txt'''    with open('output.txt', 'r+', encoding='utf-8') as file:        foreach(print_output_file, file)    print('\nEliminar consulta\n(1) Si\n(Otro)Salir sin eliminar consulta')    opcion = input('Opción: ')    if opcion == '1':        print('Ingrese las consultas a eliminar separadas por (,)')        n = input('Números: ').strip(',')        delete_consults_file([int(x.strip()) for x in n if x.strip().isdigit()])        print('\n(1) Eliminar otra consulta\n(Otro) Salir')        opcion = input('Opción: ')        if opcion == '1':            read_file_menu()def print_output_file(line):    ''' función que imprime una linea del archivo sin el salto de linea'''    print(line.strip())def delete_consults_file(n):    '''función que elimina consultas del archivo output.txt'''    with open('output.txt', 'r', encoding='utf-8') as file:        lines = [line for line in file]    lines = [l for x, l in enumerate(lines) if (x // 3) + 1 not in n]    lines = [f'Consulta {x // 3 + 1}\n' if not x % 3 else l for x, l in             enumerate(lines)]    with open('output.txt', 'w', encoding='utf-8') as file:        foreach(file.write, lines)if __name__ == '__main__':    try:        while True:            print('\nConsultas\n(1) Abrir un archivo\n'                  '(2) Ingresar consultas por consola\n'                  '(3) Leer archivo output.txt\n')            opcion = input('Opción: ')            if opcion == '1':                open_file_consult_menu()            elif opcion == '2':                new_consult_menu()            elif opcion == '3':                read_file_menu()            else:                print('No ingresó una opción válida')    except KeyboardInterrupt():        exit()