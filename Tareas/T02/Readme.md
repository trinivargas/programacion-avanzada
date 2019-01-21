  # Tarea 2: DCCasino :school_satchel:
María Trinidad Vargas

@trinivargas

Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea este, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo qué hace y qué **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

**Estos cambios no son esenciales para la simulacion.** Solo faltan para cumplir con el enunciado.
(Se me olvidaron por no llerlo taaan detalladamente)

Cambiar la linea 12 de ```juego.txt``` por ```(1 + ψ * cliente.ansiedad)``` 

Las instalaciones no tienen id propio. Para que tengan hay que hacer los mismo que en la case Persona
En el archivo ``` instalacion.py```: 
    1. importar ```count``` de la librería ``` itertools```
    2. agregar un atributo de clase ```_id```
    3. agregar un atributo ```self._id = next(Instalacion._id)``` en el ```__init__```
    
   ``` python 
   from itertools import count # después de la linea 1
   _id = count(start=0) # después de la linea 5 (habiendo agregado la linea de antes, justo después de  class Instalacion)
   self._id = next(Instalacion._id) # en el __init__() de la clase Instalacion
   
   ```

También me faltó el nombre de las instalaciones (los borré porque creía que eran inutiles,
 ya que no los usaba en ninguna parte 🤦🏼‍♀️):

Agregar en el ```__init__``` de ```Restobar``` ```self.nombre = 'restobar'```

En el ```__init__``` de ```Tarot```: ```self.nombre = 'tarot'```

En el ```__init__``` de ```Bano```: ```self.nombre = 'baño'```

En el ```__init__``` de ```Ruleta```: ```self.nombre = 'ruleta'```

En el ```__init__``` de ```Tragamonedas```: ```self.nombre = 'tragamonedas'```

### Cosas implementadas y no implementadas :white_check_mark: :x:
**Creo que esta todo implementado sin contar lo que puse arriba.** 
Pero siempre se me olvidan cosas 🤷‍♀️

* Parte <2<sub></sub>> DCCasino:
    * La clase ```DCCasino``` maneja el personal, clientes, instalaciones, juegos y actividades.
    * Luego que se acabe el tiempo llama a la clase ``` Estadisticas``` y las imprime.
    

* Parte <3<sub>1</sub>> Clientes:
    * Clase ```Cliente```, que hereda de ```Persona``` y ```Human```
    * Parte <3<sub>1.1</sub>>  Características: La ansiedad y stamina son properties y usan los atributos ```_ansiedad```, ```_stamina```
    El resto son atributos definidos en el init a través de la función ```_definir_atributos```
    * Parte <3<sub>1.2</sub>> Las personalidades están implementadas en el 
    ```__init__``` de la clase. Ahí hay una función ```definir_atributos``` que define los atributos con el valor 
    correspondiente a la personalidad.
    * Parte <3<sub>1.3</sub>> Decisiones:
    Implementada en la clase ```DCCasino```. 
    Así los clientes que no están haciendo nada toman una decisión.
    
* Parte <3<sub>2.1</sub>> Personal
    * Clase ```Personal``` que hereda de ```Persona```. Además están las
     clases ```Bartender```, ```Dealer``` y ```MrT``` que heredan de ```Personal```
   * Todas las características están implementadas. 
   * Se inicializan en la clase ```DCCasino``` 

* Parte <3<sub>3.1</sub>> Juegos
    * Clase ```Ruleta``` y ```Tragamonedas``` que heredan de ```Juego```. A su vez, esta hereda de ```Instalacion```
    * Implementada entera. 

* Parte <3<sub>4</sub>> Instalaciones:
    * Parte <3<sub>4.1</sub>> Características:
    
    Falta implementar el ```_id``` y el nombre pero están mencionados más arriba. 
    
    La ubicacion es ```destino``` que es donde deben ir los clientes para ir a la instalación.
    ```destino``` es para la fila de espera y ```coordenadas_adentro``` para realizar la actividad.
    
    Todas las instalaciones cuentan con las caracteristicas descritas en el enunciado.
    * Parte <3<sub>4.2</sub>> Tipos de instalaciones:
    Está implementado todo lo que se pide en el enunciado.
    

* Parte <4<sub></sub>> Actividades:
    * Están implementadas todas las actividades en las clases ```Conversaciones```, 
    ```TiniPadrino``` y ```Estudio``` que heredan de la clase ```Actividad``` 
    * Cada actividad tiene sus restricciones y modifica los atributos de cada cliente.

* Parte <5<sub></sub>> Interfaz gráfica:
    * Implementada entera


* Parte <6<sub></sub>> Simulacion:
    * Implementada entera

* Parte <6<sub>1</sub>> Estadísticas:
    * Implementada entera. Se calculan en la clase ```Estadisticas``` y se guardan en el archivo ``` resultados_simulacion.txt```. 
    Hay un ejemplo de los resultados en mi repositorio de la tarea.
    
* Parte <6<sub>2</sub>> Parametros:
    * En el archivo ```parameters.txt```. Implementado entero

* Parte <7<sub></sub>> Diagrama de clase:
    * En el archivo ```diagrama_clase_Vargas.pdf```

    ...
 


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```itertools ``` -> ```count ```
2. ``` colections``` -> ```deque```, ```namedtuple```
2. ```abc``` -> ```ABC```, ```abstractmethod```
3. ```random``` -> ```random```, ```randint```, ```triangular```, ```normalvariate```, ```uniform```, ```choice```, ```choices```
4. ```faker``` -> ```Factory``` (debe instalarse)
5. ``` gui``` y ```gui.entities``` -> Para la interfaz

...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```dccasino``` -> Contiene la clase ```DCCasino```
2. ```persona ``` -> Contiene la clase ```Persona```
3. ```cliente``` -> Contiene la clase ```Cliente```
4. ```personal``` -> Contiene las clases ```Dealer```, ```Bartender```y ```MrT``` que herendan de ```Personal```, también en el archivo.
5. ```instalacion``` -> Contiene la case ```Instalacion```
6. ```instalaciones``` -> Contiene las clases ```Baño```, ```Tarot``` y ```Restobar```
7. ```juegos``` -> Contiene las clases ```Juego```, ```Ruleta``` y ```Tragamonedas```
8. ```actividad``` -> Contiene las clases ```Actividad```, ```Conversacion```, ```Estudio``` y ```TiniPadrino```
9. ```estadisticas``` -> Contiene la clase ```Estadistica```
10. ```parameters``` -> Contiene los parametros externos de la simulación.


...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. El tiempo de los juegos es constante para todos los clientes.
Cada ronda del tragamonedas dura 4 minutos y cada ronda de la ruleta dura 3 
minutos. Todos los clientes juegan una sola ronda, excepto los fisico determinista 
(que juegan ν rondas solo esa vez que van al juego)

3. La capacidad máxima de los juegos es 20 personas, al igual que las 
instalaciones (excepto el Tarot que es 1). El requerimiento minimo de personal 
de cada juego es 1. En el tragamonedas para que vigile, y en la ruleta para recibir apuestas etc.

4. El tiempo de duracion de todas las actividades se aproxima al entero ya 
que se toman decisiones y realizan acciones cada minuto. Sin embargo la interfaz 
sí se actualiza cada segundo de la simulacion (16 milisegundos reales).
Cada minuto de la simulación es un segundo en la interfaz.

5. Los clientes que se mueven de una instalación a otra están en estado de 
"llegando a la simulación" ya que de otra forma no alcanzan a llegar a la entidad
en la interfaz.

6. Cada vez que se habla con Tini aumenta la p de ganar si hay almenos un dealer
coludido. Ya que la actividad de hablar con el aumenta en κ% la p de ganar.

7. Luego que un kibitzer estudie tiene probabilidad igual a deshonestidad de ir directo
a la ruleta y hacer trampa en las ν rondas.

8. Hay dos tipos de tick. Uno de la simulacion (que toma todas las decisiones) y se llama cada minuto de la simulacion (1 segundo).
Y otra de la interfaz que se llama cada segundo de la instalacion (16 milisegundos) y se encarga de mover los clientes a sus destinos.
Las imágenes de las instalaciones y juegos se manejan a parte ya que cada clase hija de instalacion tiene sus coordenadas donde llegan 
los clientes, pero estas no se mueven (solo las llama ``` tick``` del casino), por lo que no es necesario que estén definidas fuera de la clase ```DCCasino```

9. Los clientes no chocan con las instalaciones que no ingresan (sí ingresa al baño se pone arriba 
y en el retobar tambien. Y para ponerse delante de un tragamonedas pasa por encima de otros). Pero por la distribución
del mapa no puede pasar por encima de otra instalacion.

10 Los clientes conversan solo en un espacio determinado. Igual que las otras actividades.
...

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://dzone.com/articles/python-create-fake-data-faker: crea nombres de personas. Está implementado en el archivo (dccasino.py) en las líneas 52, 55, 59, 63, 115 y 116 y crea nombres falsos para los clientes y personal



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).