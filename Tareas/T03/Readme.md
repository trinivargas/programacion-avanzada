# Tarea 03: Electromatic 

Las funciones ```potencia_real()``` actualizan los atributos ```potencia_ideal``` y ```potencia_real```


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea este, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

* Agregar en la linea 63 de ``eliminar_nodo.py``: ``conexiones = Conexiones()`` 
para que no se caiga, ya que no terminé la funcion.

* Las siglas que se piden para el sistema es la que sale en la base de datos 
son: sing, sic, magallanes y aysen.

* Cada entidad  ``Elevadora``, ``Transmision``, ``Distribucion`` y ``Casa``
es un nodo, que uno de sus atributos es ``self.conexiones`` que es una Lista Ligada.
Además las Elevadoras tienen un atributo self.centrales, que también es una ListaLigada
 que guarda las conexiones que tiene con cada ``Central``
 
 * Los nodos de las ``ListaLigada()`` tienen ``id_``,``entidad=None`` y
  ``distancia=None``. La entidad es una instancia de algun elemento de la red.
 
* En la consola hay distintos menus para agregar y eliminar los nodos y las aristas. 
Es por esto que solo se eliminan los nodos sin conexiones una vez que se quieren hacer ls consultas.
Así se pueden agregar los nodos y luego modificar las aristas sin problema.

* Cuando me refiero a potencia real es la que en verdad le llega a cada nodo, y 
la potencia ideal, la que le debería llegar para satisfacer el consumo propio y el de todos los nodos hijos.
 

<Descripción de lo qué hace y qué **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte <3>: Hecha completa
    * Parte <3<sub>1</sub>> Cálculo de la demanda de la red: Cada nodo tiene una property
    llamada ``potencia`` que retorna el valor de la potencia demandada por el nodo 
    (el consumo propio más la que necesita para que a cada nodo hijo le llegue lo que
    consume, y actualiza el valor de ``p_ideal`` de cada nodo hijo)
    * Parte <X<sub>3.2</sub>> Flujo de potencia en la red: Además cada entidad tiene
    una funcion ``calcular_potencia_real()`` que actualiza los valores de ``p_real`` 
    de cada nodo hijo. y tambien hace que cada nodo hijo calcule la de sus nodos hijos.
    
    ... 
    
* Parte <4>: Me faltó hacer <insertar qué cosa faltó>
    * Parte <X<sub>4.1</sub>> Agregar y remover aristas: Hecho completo
    * Parte <X<sub>4.2</sub>> Agregar nodos: Hecho completo
    * Parte <X<sub>4.3</sub>> Remover nodos: 
    Primero se quitan todos los nodos que el usuario quiere, y luego se puede confirmar.
    Si esta configuracion lanza algún error, el programa no deja realizar los cambios.
    Se pueden desconectar bien las centrales, elevadoras y casas. Faltaron las subestaciones
    de distribucion y transmision.
    
    
    ...

* Parte <5>:Consultas Hecho completo
    * Parte <X<sub>5.1</sub>> Enerǵıa total consumida en una comuna: No me quedó claro
    el string que se usa, ya que al principio dice "un str de la comuna", y después un id.
    Sin embargo, el programa pide el nombre de la comuna ej. Pica, y retorna la potencia real
    total: suma de la potencia de cada subestacion de distribucion (que incluye las casas conectadas y la perdida)
    * Parte <X<sub>5.2</sub>> Clientes con mayor consumo: Retorna el cliente con mayor 
    consumo de la red, pero del consumo real, es decir de lo que le llega por la red.
    * Parte <X<sub>5.3</sub>> Clientes con menor consumo: Retorna el cliente con
    menor consumo que está conectado al sistema. Si ninguno tiene potencia mayor a 0
    retorna None
    * Parte <X<sub>5.4</sub>> Potencia perdida en transmisíon: Calcula la potencia perdida
    desde la elevadora e incluye los caminos de todas las distribuciones a las que puede estar
    conectado.
    * Parte <X<sub>5.5</sub>> Consumo de una subestacíon: hay que elegir primero entre
    tipos de subestacion, ya que se pueden repetir los id`s, y retorna la potencia real que demanda.

    ...

* Parte <6> Excepciones: Hecho completo
* Parte <7> Testing: Hecho completo. Prueba todas las consultas y los errores. 
Además prueba Consumo de una subestacíon para una distribucion y una transmision.
* Parte <8> Interaccion con consola: Hecho completo. Hay un menu para las consultas y el
resto para modificar la red. En el mismo menu que se agrega se puede probar los cambios,
es decir, se hacen los cambios y si no se confirman no se realizan.
Como mencioné más arriba, primero se crean loss nodos, y después se pueden conectar en 
los otros menus.

    ...

* Parte <X<sub>n</sub>>: Me faltó hacer <insertar qué cosa faltó>

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. En este módulo sale
el path de la base de datos que se va a usar.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```csv```-> ```reader``` Para abrir la base de datos
2. ```unittest```-> ```TestCase``` y ```TestCase``` en testing

...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```estructuras.py```-> Contine a ```Nodo```, ```ListaLigada```, ```NodoConexion```, ```Conexiones```
1. ```entidades.py```-> Contine a ```Casa```, ```Distribucion```, ```Transmision```, ```Elevadora```, ```Central```
1. ```sistema.py```-> Contine a ```Sistema``` Hecha para poder manejar el grafo y calcular la potencia y otros datos
1. ```sistemas.py```-> Contine a ```Red``` Contiene todos los sistemas y funciones para modificarlos.
1. ```errores.py```-> Contine a ```InvalidQuery```, ```ForbidenAction```, ```ElectricalOverload```
1. ```menu.py```-> Contine a ```Menu```
1. ```consultas.py```-> Contine a ```Consultas``` Contiene las funciones de las consultas
1. ```crear_nodos.py```-> Contine a ```CreacionNodos``` 
1. ```eliminar_nodo.py```-> Contine a ```EliminarNodo```
1. ```crear_arista.py```-> Contine a ```ConectarNodos```
1. ```eliminar_arista.py```-> Contine a ```EliminarArista```
1. ```main.py``` instancia la clase Red y Menu
Los últimos 4 archivos fueron creados para la interaccion con consola, y poeder probar cambios
y hacerlos de forma permanente.
2. ```testing.py```-> Contine a ```Test``` 

...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. La consulta de energia en una comuna recibe un str con el nombre de la comuna 
porque en el enunciado dice "dado un string de comuna"
2. Los nodos sin conexión se eliminan antes de las consultas. Así se pueden hacer todos los cambios
necesarios sin tener problemas.
3. No hay error si se trata de eliminar una conexión válida si no existe, ya que después de la funcion
va a estar desconectado.
4. 

...

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>


-------



**EXTRA:** si van a explicar qué hace especificamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

```python
class Corrector:

    def __init__(self):
          pass

    # Este método coloca un 6 en las tareas que recibe
    def corregir(self, tarea):
        tarea.nota  = 6
        return tarea
```

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

```python
def funcion(argumento):
    """
    Mi función hace X con el argumento
    """
    return argumento_modificado
```
Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. Contenidos del ramo. Específicamente de grafos (semana 7) 
   * Usé la clase Node y de la clase Grafo use DFS
   * De la semana 6 usé ListaLigada




## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).