# Tarea 0: DCCorreos :school_satchel:

María Trinidad Vargas
@trinivargas

## Consideraciones generales :octocat:

Al iniciar el programa, se inicia una instancia de la clase ```Servidor``` la que contiene  todas las funciones pedidas.

Esta clase se mueve entre los distintos menús y crea las instancias de ```Usuario```, ```Correo``` y ```Evento```.


En la mayoría de los menús si la opción ingresada no es válida, se vuelve a imprimir el menú hasta que ingrese una opción válida. Si no entrega la opción por defecto.

Al abrir los mails y eventos, hay que entregar un input (puede ser vacío) para que no se imprima al tiro todos los mails o el calendario completo, y así, poder leerlos más facilmente.

Para modificar un evento, primero hay que abrirlo y ahí está la opción de modificarlo. Si no es el dueño devuelve al calendario e imprime 'No se puede modificar'.


### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte <3<sub>1</sub>>: Hecha completa
* Parte <3<sub>2</sub>>: Hecha completa
* Parte <3<sub>3</sub>>: Hecha completa

    ...

* Parte <3<sub>4</sub>>:
    * Parte <3<sub>4.1</sub>>: Hecha completa
    * Parte <3<sub>4.2</sub>>: Me faltó buscar por fecha, pero si filtra los eventos por nombre y etiqueta (solo una).

    ...

* Parte <3<sub>5</sub>>: Hecha completa

    ...

* Parte <4<sub>1</sub>>: Hecha completa



## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```-> ```randint``` en codificar(texto) de la clase Servidor.
2. ```datetime```-> ```datetime``, ```timedelta``` en los eventos (para las fechas).

...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```servidor```-> Contine a ```class Servidor```
    La clase servidor contiene el programa.
2. ```clases```-> Contine a ```class eUsuario```, ```class Correo```, , ```class Evento```
    Cada clase contiene la información y algunas funciones para inicializar la instancia.

...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. No pueden haber dos eventos al mismo tiempo ni se puede repetir el nombre porque el enunciado dice: 'no pueden haber dos eventos con la mismas fechas y el mismo nombre.'
2. No se considera la opción que el cuerpo del correo tenga caracteres que no sean ASCII.
3. La direccion de servicio debe ser real, es decir, si tiene más de un punto debe haber texto entre estos.

...

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>


-------




** Se me olvidó explicar que hacen las funciones** Pero acá van las más importantes:


1. ```class Servidor```: Contiene el programa y está dividida en grandes partes separadas por #.


    1.1 Inicio y correo. Contiene el menú de inicio, el registro de nuevo usuario y el inicio de sesión.

    1.2 Menú DCCorreos. Tiene el menú de bandeja de entrada, nuevo correo y calendario, además de las funciones para crear un nuevo correo.

    1.3 Calendario. Tiene la función que imprime el calendario y busca por caracteristicas.

    1.4 Eventos. Tiene las funciones para abrir un evento, crear nuevos eventos y modificar uno existente.

    1.5 Codificación: Contiene dos funciones, una para codificar un texto y otra paa decodificar.

    1.6 Cargar datos: lee los tres archivos de usuarios, correos y eventos y los carga a la clase ```Servidor```.


2. ```class Correo ```: Contiene la imformación de los correos y el ```__str__()``` para imprimirlo.

3. ```class Usuario```: Contiene la dirección y la contraseña. Todas las instancias se guardan en un diccionario definido en la clase Servidor.

4. ```class Evento```: Contiene las funciones para crear un nuevo evento y para modificarlas.


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

0. No usé ningún código de internet.



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).