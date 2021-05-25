# Tarea 1: DCCumbre Olímpica :school_satchel:

## Consideraciones generales :octocat:

Actualmente este codigo te permite jugar perfectamente, y el flujo del programa parece estar bien. No se ha hecho un examen muy exhaustivo pero el programa no se cae, por lo que los errores posibles pueden ser algun item no hecho estrictamente bajo las especificaciones del ensayo, o valores mal puestos.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Flujo del programa<sub>2</sub>: Hecha completa :white_check_mark:
* Menús<sub>3</sub>: Hecho completo, para este item se hizo una libreria que contiene todos los menús y sub menús, para hacer más limpia la otras del codigo. :white_check_mark:
    * Menú de Inicio<sub>3.1</sub>>: Hecha completo 
    * Menú Principal<sub>3.2</sub>>: Hecho completo
        * Menú Entrenador<sub>3.2.1</sub>>: Hecho completo
* Entidades<sub>4</sub>: :white_check_mark:
    * Delegaciones<sub>4.1</sub>: Hecha completo, cabre recalcar que en esta entidad se uso Herencia, polimorfismo y metodos abstractos, pues presento una gran utilidad.
    * Deportistas<sub>4.2</sub>: Hecho completo; en esta entidad se usaron properties para cuidar que no se pasen de ciertos valores los atributos de cada deportista. Esta clase es independiente a las demas
    * Deportes<sub>4.3</sub>: Hecho completo, tambien se aprovecho de usar la herencia para optimizar codigo, composición y clases abstractas para modelar como tenia que ser cada sub-deporte.
    * Campeonato<sub>4.4</sub>: Hecho completo, Campeonato resulto ser la gran compiladora de todas las demas clases, por lo que tuvo relaciones de agregación, y composición con todas las demás (mejor evidenciado en el diagrama de clases)
* Archivos<sub>5</sub>: Hecho completo. :white_check_mark:
    * delegaciones.csv<sub>5.1</sub> si se le cambia el orden al header se lee de todas maneras, se puede observar el proceso en el archivo ```cargar_datos.py```.
    * deportistas.csv<sub>5.2</sub> Al igual que el punto anterior, se logro completamente leer este archivo.
    * resultados.txt<sub>5.3</sub> Hecho completo.
    * parametros.py<sub>5.4</sub> Hecho completo.
    


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos en el directorio de la tarea.
1. ```delegaciones.csv``` en ```el mismo directorio que el resto del codigo```
2. ```deportistas.csv``` en ```el mismo directorio```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```uniform```
2. ```abc```: ```"abstract method y ABC```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```deporte```: Contiene a ```Deportistas``` y ```Deportes``` con su correspendondiente herencia.
2. ```delegaciones```: Contiene ```Delegaciones```y sus clases heredadas (IEEEsparta y DCCrotona).
3. ```funciones```: Hecha para optimizar ciertas acciones que se repetian durante todo el codigo, por ejemplo, contiene la funcion ```ingresar_input```, la cual es a prueba de errores y sirve para todos las partes en las que haya que ingresar un comando.
4. ```menu```: Hecha para definir todos los menús como funciones y llamarse entre ellos.
5. ```cargar_datos```: Hecha para cargar los datos de los csv siempre y cuando haya un header que lo especifique.
6. ```parametros```: Hecha para almacenar la mayoria de los parametros que se usan, por ejemplo las bonificaciones y poneradores de la libreria campeonato.
7. ```campeonato```: Esta libreria solo contiene la clase Campeonato, pero dada la extensión de esta parecía optimo dejarla en una librería propia.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Algunos numero se pueden poner directamente en el codigo, pues hace mensión a los más importantes en el enunciado. Esto no significa que no use la librería parametros, solo que en algunos momentos fue más optimo escribir algunos numero directamante en el codigo y no como algo aparte.

2. En el item Menús, al ingresar apódo, asumí que la linea que dice "se deberá pedir un nombre de usuario y un nombre de rival que sólo consideren caracteres alfanuméricos sin distinción entre mayúsculas y minúsculas." se refiere a que el usuario no debe preocuparse en ingresar minusculas o mayusculas, no en que el nombre debe tener solo mayusculas o solo minusculas. Esto porque se presta para interpretaciones como que lo que se quiere es pedir un nombre sin que importe si es mayuscula o minusculas, y no un nombre solo con mayusculas o solo con minusculas

3. Asumí que se puede entrenar y comprar tecnologia sin importar si los atributos ya estan en su maximo, pues en el enunciado no dice lo contrario

4. Durante el codgio existen algunos comentarios que me parecieron importantes para destacar y encontre util que estuvieran en el contexto del codigo.

-------

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
