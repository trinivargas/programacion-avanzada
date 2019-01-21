# Tarea 1: Nombre de la tarea Cruncher Flights

María Trinidad Vargas
@trinivargas

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo qué hace y qué **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

Cambiar la linea 205 que originalmente tenía ``` p_ids = sorted(p_miles.keys(), key=lambda x: p_miles[x])[- n:]``` por ```p_ids = sorted(p_miles.keys(), key=lambda x: p_miles[x])[- n:][::-1]```.
**_Falta ```[::-1]```_** Así entrega el resultado en orden decreciente y no creciente.

...
### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte <2<sub>1</sub>>: Lectura de archivo: Hecha completa. Lee todos los archivos y los retorna en tuplas. Por defecto la carpeta es ```large``` y se puede cambiar en la linea 9. Y el archivo de ```Travels``` es ```flights-passengers2.csv``` y se puede cambiar en la linea 48.

* Parte <2<sub>2</sub>>: Consultas Hecha completa

    * Parte <2<sub>2.1</sub>> Formato de consultas

    El programa no lee consultas abiertas de archivos en una lista, solo lee una consulta con un diccionario por linea. (Como ```queries.txt```
    Pero sí acepta ambos formatos de consultas: solo un diccionario o varios en una lista en las consultas ingresadas por consola)

    Consultas de archivos de la forma: ``` {"load_database": ["Airports"]} ```

    Consultas de archivo por consola :``` {"load_database": ["Airports"]}``` o ``` [{"load_database": ["Airports"]},{"load_database": ["Flights"]}]

    * Parte <2<sub>2.2</sub> Consultas que retornan otra base de datos:

        * 1.- ```load_database(db_type)```: retorna cada base de datos como generador con namedtuple (```Person```, ```Flight```, ```Travel```, ```Airport```). Usa la función ```direction_file(*args)``` que retorna el path del archivo a abrir.

        * 2.- ```filter_flights(*args)````: Usa la función ```operators(*args)``` que retorna una función con el operador pedido y la función ```flight_distance(*args)```.

        * 3.- ```filter_passengers(*args)```: Considera solo el aeropuerto de destino de cada viaje. Usa la función ```flight_airports(*args)``` que retorna todos los vuelos que llegaron al aeropuerto.

        * 4.- ```filter_passengers_by_age(*args)```

        * 5.- ```filter_airports_by_country(*args)```

        * 6.- ```filter_airports_by_distance(*args)``: Usa la función ```distance(*args)```.

    * Parte <2<sub>2.3</sub>> Consultas que no retornan otra base de datos:

        * 1.- ```favourite_airport(*args)````: Considera solo los aeropuertos de destino.

        * 2.- ```passenger_miles(*args)```

        * 3.- ```popular_airports(*args)```: Retorna el resultado en una lista sin ningún orden en específico. Usa la función ```number_passengers_airport(*args)```.

        * 4.- ```airport_passengers(*args)```: Usa las funciones ```one_airport_passengers(*args)``` y ```operators(*args)```.

        * 5.- ```furthest_distance(*args)```: Después de hacer el cambio mencionado al principio, entrega el resultado en forma decreciente. Usa la función ```airports_distance(*args)```.


...

* Parte <3>: Interacción con consola: Hecha completa

    El menú tiene 3 opciones: (1) Abrir archivo que se puede cambiar a ```queries.txt```eliminando el ```#``` de la linea 256. (2) Ingresar consulta por consola y (3) Abrir archivo ```output.txt```.

    * Parte  <3<sub>1</sub>>: Abrir archivo con consultas. Solo acepta consultas del tipo de ```queries.txt``` como se mencionó anteriormente. El menú está hecho en la función ```open_file_consult_menu()``` el cual usa las funciones ```open_file()```, ```read_consult(*args)```, ```consults()```, ```consults_dictionary()``` y ```consults_results(*args)```. Para imprimir los resultados se usa la función ```foreach(*args)``` con ```print_result(result)```.

    * Parte <3<sub>2</sub>>: Ingresar consultas por consola. Acepta consultas en listas o una en diccionario. Usa las funciones ```new_consult_menu()```, ```new_consults_results(*args) ```, ```read_consult(*args)```. Para imprimir el resultado se usa ```foreach(*args)``` con ```print_result(*args)```. Y para guardar las consultas se usa la función ```save_consult(*args)``` también con ```foreach(*args)``` y ```string_result(*args)```. Las funciones ```string_result(*args)``` y ```print_result(*args)```.

    * Parte <3<sub>3</sub>>: Abrir archivo ```output.txt``` Abre el menú ```read_file_menu()```

...

* Parte <4>: Archivos relacionados a la tarea. Hecha completa.

    * Parte <4<sub>1</sub>> Archivo ```output.txt```: Guarda las consultas de la forma:

    ```Consulta X\n```
    ```{consulta: *args} \n```
    ```< class >, resultado separado por ; ```


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```collections```-> ```namedtuple``` y ```Counter```
2. ```datetime```-> ```datetime```
3. ```math```-> ```sin```, ```asin```, ```cos``` y ```radians```
4. ```itertools``` -> ```tee```
5. ```os``` -> ```listdir```, ```getcwd```
6. ```types``` ->  ```GeneratorType```

...

### Librerías entregadas
```iic2233_utils``` -> ```parse```, ```foreach```

...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. La función ```favourite_airport(*args)``` solo considera los aeropuertos de destino ya que el enunciado dice 'del aeropuerto _**al**_ cual ese pasajero viaj́o ḿas veces'.

2. La función ```popular_airports()``` retorna lista ya que en el type hinting dice ``` funcion -> list ``` (Aunque después en la descripción dice tupla).
Tampoco dice en el enunciada un orden específico del resultado por lo que se entrega en orden creciente.


...

PD: La funcion ```filter_passengers(*args)``` se agregó varios sets y diccionarios para hacerla más eficiente.

Al correrla con la base de datos large se demora 2 segundos aprox. Ya que solo con el uso de ```filter``` y ```map``` se demoraba 6 s con la carpeta medium.

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://stackoverflow.com/questions/466345/converting-string-into-datetime: este hace X cosa y está implementado en el archivo main.py en la línea 30 y entrega un string en forma datetime


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
