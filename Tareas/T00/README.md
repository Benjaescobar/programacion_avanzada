# Tarea 00: DCCombateNaval :ship:

## Consideraciones generales :octocat:


La tarea 00 tiene implementada todo lo pedido, excepto por algunos print() que no imprimen exactamente lo pedido. No se han detectado errores que hagan que el programa se caiga, por lo que en general parece que el funcionamiento esta bastante bien.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* **Flujo de programa**<sub>2</sub>: Hecho completo

* **Menus**<sub>3</sub>:
    * Menu de inicio<sub>2.1</sub>: Hecha completo
    * Menu de juego<sub>2.2</sub>: Hecho completo

* **Reglas**<sub>4</sub>: Hecho completo

* **Elementos**<sub>5</sub>:
    * Mapas<sub>5.1</sub>: Hecha completo
    * Barcos<sub>5.2</sub>: Hecho completo
    * Bombas<sub>5.3</sub>: Hecho completo

* **Crear**<sub>6</sub>: 
    * Crear<sub>6.1</sub>: Hecho completo
    * Oponente<sub>6.2</sub>: A diferencia de lo pedido, el tablero se imprime cuando el turno del computador se acaba, ademas, se imprime un mensaje que no contiene las coordenadas. (Esto fue porque no habia entendido ese requisito, pero es muy simple de arreglar.)

* **Puntaje**<sub>7</sub>: Hecho completo

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```puntajes.txt``` en ```T00```
2. ```tablero.py``` en ```T00```
3. ```parametros.py``` en ```T00```


## Librerías :books:
### Librerías externas utilizadas
Solo se utilizaron las librerias "Built in" que estaban permitidas para la tarea.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```juego.py```: Es el responsable estrictamente de jugar, es decir, comienza desde el -- menu de juego -- y se termina cuando se gana, rinde, pierde o cierra el programa. Retorna alguno de esos 4 comandos de modo que en el **main.py** se ejecutan distintas opciones.
2. ```bombas.py```: Contiene 4 funciones principales que corresponden a las 4 bombas disponibles en el juego, las cuales son llamadas en el modulo **juego**<insertar descripción **breve** de lo que hace o qué contiene>
3. ```funciones.py```: Hecha para hacer mas limpio el codigo principal, contiene las funciones checkear_apodo, crear_mapa y ranking.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Supuse que no era necesario imprimir las coordenadas que disparo el usuario, pues en el enunciado no recuerdo haber leido que lo fuera, y en la consola se pueden ver las ultimas coordenadas que ingresaste.
-------