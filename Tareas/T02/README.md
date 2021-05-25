# Tarea 02: DCCumbia :school_satchel:

## Consideraciones generales :octocat:

Actualmente se puede jugar el juego en todas las dificultades, con musica, se puede pausar y jugar multiples rondas, además el puntaje queda registrado. Sin embargo hay un par de funcionalidades (más abajo saldra en más detalle) que no funcionan muy bien.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* **Flujo Del Programa<sub>2</sub>:** Hecho casi completo, si se cierran las ventanas el juego se cae, y no queda registrado el puntaje. De esa forma conviene usar los botones de la interfaz para moverse a traves de las ventanas.
* **Mecánicas<sub>3</sub>:**
    * Pasos de baile<sub>3.1</sub>: Hecha casi completa, por alguna razón que no logre identificar (puede que tenga que ver con la capacidad de presionar declas de mi computador), el paso combinado arriba-izquierda-abajo y el paso arriba-derecha-abajo no se puede presionar, pero este es el unico paso y me parece que tiene que ver con el computador.
    * Tipos de Flechas<sub>3.2</sub>: Me faltó hacer el efecto de la flecha hielo, pero todas las demás funcionan bien.
    * Combo<sub>3.3</sub>: Hecho completo.
    * Dificultad<sub>3.4</sub>: Hecho completo.
    * Puntaje<sub>3.5</sub>: Hecho completo.
    * Fin del nivel<sub>3.6</sub>: Hecho completo.
    * Fin del juego<sub>3.7</sub>: Hecho casi completo, pues el puntaje solo se registra al presionar el boton volver.
* **Interfaz Grafica<sub>4</sub>:**
    * Modelacion del programa<sub>4.1</sub>: El programa esta bien modulado, se usan señales para practimente todas las partes logicas de forma que se trabajan en el back_end además de Qthreads para las tareas que lo necesitaban, y Qtimers. Sin embargo ciertas partes del back_end poseen mucho acomplamiento, para ayudar a eso se creo el modulo ```funciones.py``` que ayuda a modulizar. en la seccion Ejecución se explica más en detalle.
    * Ventanas<sub>4.2</sub>: Hecho completo.
        * Ventana de Inicio<sub>4.2.1</sub>: Hecho completo.
        * Ventana de Juego<sub>4.2.2</sub>: Me falto hacer que el boton salir volviera a la ventana de inicio, por lo que el boton salir te saca del juego, todo lo demás funciona bien.
        * Ventana de Ranking<sub>4.2.3</sub>: Hecho completo. (se vuelve al inicio presionando *volver*)

* **Interacción con el Usuario<sub>5</sub>:**
    * Click<sub>5.1</sub>: Hecho completo.
    * Atrapar Flechas<sub>5.2</sub>: Hecho completo.
    * Movimiento Pinguirines<sub>5.3</sub>: Hecho completo.
    * Pausa<sub>5.4</sub>: Hecho completo.
    * Cheatcodes<sub>5.5</sub>: Hecho completo.
    * Drag and Drop<sub>5.5</sub>: Hecho completo, pero quiero recalcar que en mi computador (Mac) no funciono en ocasiones, por lo que tuve que programarlo bien en un Windows. Digo esto por si llegara a sucederles tambien. Además asumí algo que esta especificado en los Supuestos y consideraciones adicionales

* **Archivos<sub>6</sub>:** Hecho completo.
    * Sprites<sub>6.1</sub>: Hecho completo.
    * Songs<sub>6.2</sub>: Hecho completo. (La carpeta debe ser creada, pues ignore la carpeta entera.)
    * ranking.txt<sub>6.3</sub>: Me falto hacer que el archivo se creara, por lo que viene incluido en el repositorio.
    * parametros.py<sub>6.4</sub>: Hecho casi completo. Es posible que algunos parametros menores no estesn, pero los más importantes estan aqui.

* **Bonus<sub>7</sub>:** abajo solo salen los bonus hechos.
    * Cheatcodes adicionales<sub>7.2</sub>>: Hecho completo.
    * Puffles<sub>7.4</sub>>: Acabo de leer que necesitan estar completos, de todas formas lo dejo aquí para que sepan que actualmente solo se pueden adquirir y dropear en la pista de baile los puffles, pero no bailan.

* **Avance en Tarea<sub>7</sub>:** Hecho completo.

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe agregar los siguientes archivos:
*La carpeta songs debe ser creada tambien.*
1. ```cancion_1.wav``` en ```songs``` 
2. ```cancion_2.wav``` en ```songs```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5``` (debe instalarse)

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

#### BACK END
1. ```logica_ventanas.py```: Contiene a ```VentanaJuegoLogica```, ```VentanaResumenLogica```, que contienen metodos relacinados con la logica de las ventanas.
2. ```flechas.py```: Contiene los labels especiales de ```PinguirinTienda``` y ```PinguirinBaila```,  ademas de la clase Flecha, la que es un QThread que permite que las flechas se muevan.
3. ```funciones.py```: Hecha para poner las funciones que pueden considerarse acopladas. En general cuando se usa una de estas funciones se comenta en el codigo.
4. ```music_player.py```: Solo contiene la clase que permite reproducir y pausar la musica.
#### FRONT END 
Los siguientes modulos se explican por si solo con su titulo, basicamente son clases heredadas de QWidget con conexiones entre ellas y entre el back_end
1. ```ventana_inicial.py```
2. ```ventana_juego.py```
3. ```ventana_ranking.py```
4. ```ventana_termino_juego.py```

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:
### Supuestos

1. Supuse que para el drag and drop, se puede tener zonas fijas para poner pinguirines, y que pueden ser limitadas. Esto lo hice por comodidad en el codigo ya que de la forma en que lo hice, mi modulo ```ventana_juego.py``` hubiera quedado muy grande al asignar muchos puestos libres. Creo que es valido pues no prejudica a la acción que se espera que hagamos, por otro lado, el programa se pone muy lento al tener hartos pinguirines.
2. Asumí que en la seccion **3.5 Puntaje** pasos_totales corresponde a la suma entre pasos_correctos y pasos_incorrectos. Creo que el Enunciado no dice nada al respecto por lo que quizas esta bien, pero quiero comentarlo de todas formas.
3. Asumí que los pinguirines solo bailan al hacer un paso correcto, esto pues en la issue #936 dice eso.
4. Supuse que el flujo del programa puede funcionar solo con botones, pues no encontre en el Enunciado que se dijiera lo contrario y me parece razonable.
5. Asumí que los pinguirines luego de hacer un paso vuelven a su posicion neutra despues de un tiempo corto, a pesar de que en el Enunciado dice que deben volver entre medio de dos pasos, pues me parece mas razonable que cada paso dure un tiempo pequeño, y de esa forma tambien se cumple el requisito pedido.

### Consideraciones

1. Una consideración importante es que en la funcion ```crear_flechas_prob``` y ```chequear_teclas``` del modulo ```funciones.py``` estan muy acopladas, es decir, contienen muchos if-elif. Esto en un principio se puede ver muy molesto pero quiero recalcar que, al entender la logica de un if, se entiende muy claro lo logica de todos los demás (en chequear_teclas deje un gran comentario pero no alcance a hacerlo en crear_flechas_prob).
2. Algunos pasos de 3 teclas no funcionan a pesar de que el codigo esta bien. me parece que tiene que ver con el computador, pero quizás estoy equivocado. La logica de los pasos de 3 teclas se encuentra en la linea 288 del modulo ```funciones.py``` en caso de que se quiera revisar.

-------

## Referencias de código externo :book:
Para realizar mi tarea me inspire en el código de:
1. https://learndataanalysis.org/create-label-to-label-drag-and-drop-effect-pyqt5-tutorial/: este hace el drag and drop y está implementado en el archivo <flechas.py> en las líneas 79 a la 109. basicamente aprendí con este tutorial de que forma se puede hacer un drag and drop entre labels. Y lo implemente de forma que la tienda lograra hacer eso.


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
