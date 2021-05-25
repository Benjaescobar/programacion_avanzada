# Tarea 03: DCColonos :school_satchel:

## Consideraciones generales :octocat:

Mi Tarea puede cargar la sala de espera y esperar a que se conecte la cantidad de usuarios del juego.  una vez cargada la sala de juego, se puede; lanzar dados, comprar casas, comprar caminos y terminar el turno, Pero no se puede comprar cartas de desarrollo. una vez finalizada la partida se cierra la ventana y carga la ultima, pero no se ve el ranking.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* **Flujo Del Programa<sub>2</sub>:** Hecho casi completo, el flujo del programa es el pedido, sin embargo no se pueden realizar algunas acciones y no se puede volver a jugar. Ademas, si se cierra alguna ventana el juego se cae.
* **Mapa<sub>3</sub>:** Hecho completo, se puede ver en el modulo ```tablero.py``` de cliente las clases que lo conforman, y tambien en ```nodos.py``` en el servidor, donde se tiene toda la logica para aprobar construcciones y ver las conexiones entre todos los objetos.
* **Reglas del Juego<sub>4</sub>:**
    * items del juego<sub>4.1</sub>: Hecho casi completo
        * Tipos de cartas<sub>4.1.1</sub>: Las materias primas existen enteras, pero las cartas de desarrollo no fueron completadas.
        * Carreteras<sub>4.1.2</sub>: Hecho completo, pero podria haber algun error no detectado
        * Chozas<sub>4.1.3</sub>: Hecho completo, aunque por alguna razon, en algunas oportunidades no aparecen las 2 chozas iniciales y solo aparece una, la logica para crear estas chozas esta en el modulo ```servidor.py``` linea 314, en el metodo ```crear_mapa.py```.
        * Banco<sub>4.1.4</sub>: El banco hace todo lo pedido menos vender cartas de desarrollo.
    * Desarrollo del juego<sub>4.2</sub>: Hecho completo.
        * Preparar el mapa<sub>4.2.1</sub>: Hecho completo.
        * Comienza la partida<sub>4.2.2</sub> Se añaden correctamente las chozas y carreteras, sin embargo no se reparten las materias primar acorde a la posicion, simplemente se entrega una cantidad x de recursos a cada jugador.
        * Lanzamiento de dados<sub>4.2.3</sub>: Falto hacer lo pedido para cuando sale el numero 7, pero lo demas funciona bien.
        * Acciones posibles durante el turno del jugador<sub>4.2.4</sub>: Solo se pueden comprar chozas y caminos.
        * Fin del turno<sub>4.2.5</sub>: Se termina el turno y le toca a otro jugador, pero no se puede volver a jugar si es que alguno gana, y se les avisa a los otros jugadores que les toca solo mediante el **turno actual** que aparece en la parte superior derecha.
* **Networking<sub>5</sub>:**
    * Arquitectura Cliente Servidor<sub>5.1</sub>: Hecho completo.
        * Separacion funcional<sub>5.1.1</sub>: Hecho completo, ningun archivo requiere de uno que este en la otra carpeta, el unico detalle es que el servidor se ejectuta desde ```servidor.py``` y no existe un ```main.py```.
        * Conexion<sub>5.1.2</sub>: Hecho completo,  pero el host y port estan definidos en ```servidor.py``` para el servidor y ```main.py``` para el cliente, no estan el parameters.json.
        * Envío de información <sub>5.1.2</sub>: Hecho completo. (fue horribe pero funciono jeje.)
        * logs del servidor <sub>5.1.5</sub>: Hecho completo. (es posible que se me haya pasado uno pero en general se estan printeando cosas constantemente.)
        * Desconexion repentina<sub>5.1.6</sub>: No se hizo. :(
    * Roles<sub>5.2</sub>: Hecho completo.

* **Interfaz<sub>6</sub>:** Hecho completo.
    * Sala de espera<sub>6.1</sub>: No se porque, a veces el primer usuario no ve los usuarios que se conectan, pero el segundo simepre los ve.
    * Sala de juego<sub>6.2</sub>: Hecho completo. (aunque algunos botones no sirven para nada [carta desarrollo y intercambio])
    * Fin de partida<sub>6.3</sub>: Se muestra pero no se puede volver a jugar.

* **Archivos<sub>7</sub>:** 
    * parametros.json<sub>7.2</sub>>: Hecho completo en cliente y servidor.

* **No se hicieron bonus ni avance de tarea**

## Ejecución :computer:
Para poder ejecutar la Tarea se debe ejecutar en un terminal el archivo ```servidor.py```, pero hay que tener en cuenta que se debe hacer desde el directorio de la carpeta que contiene a la carpeta ```server.py``` y ```client.py```. Es decir, desde una terminal debe correrse de la forma ```python3 server/servidor.py```.

Una vez ejecutado el servidor, se debe ejecutar 2 clientes con la misma logica mencionada anteriormente, por lo que en un terminal se debe usar el comando ```python3 client/main.py```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```: Se usaron muchas herramientas que esta brinda (debe instalarse).
2. ```json```: json.loads/json.dumps/json.load/json.dump. viene incluida en python por lo que no debe instalarse.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

#### SERVIDOR
1. ```logica_servidor.py```: Contiene a varios metodos que son de logica en el servidor.
2. ```nodos.py```: Contiene los objetos ```Nodo```(choza), ```Camino``` y ```Hexagonos```, que sirven para la logica de conexion entre nodos y para habilitar o no construcciones.

#### CLIENTE

##### FRONT_END
1. ```tablero.py```: Contiene varias clases "especiales", como ```Mapa```, ```WidgetInfo``` que tienen caracteristicas escenciales para poder por ejemplo comprar chozas y caminos (mousePressEvent)


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. LA TAREA DEBE SER CORRIDA DESDE EL DIRECTORIO T03 (toda la carpeta) PUES TODOS LOS PATHS ESTAN PENSADOS DESDE AHI
2. El juego funciona perfecto con 2 jugadores, pero nunca tuve la oportunidad de probarlo con mas a pesar de que supuestamente se puede (quiero decir que en general todo esta hecho para funcionar con mas jugadores pero no lo he probado por lo que quizas haya un error que no he detectado). No se si es valido que no funciones con mas pero creo que al hacer que funcione bien con 2 logre aprender mucho de networking, que es el primer responsable de ampliar el numero de jugadores.
3. Dado a que no se puede intercambiar recursos, recomiendo cambiar los parametros de cantidades_iniciales ubicados en la linea 25 de parameters.json en la carpeta ```server```. de forma que se haga mas ameno el juego en cuanto a realizar compras y ver el fluj del programa.

-------

## Referencias de código externo :book:

Desde la linea 61 hasta la 141 de el archivo servidor.py me inspire en la ayudantia 11 de Networking, complementandolo con el protocolo pedido en nuestra tarea. Estas lineas se encargan de aceptar usuarios y empezar a escucharlos.

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
