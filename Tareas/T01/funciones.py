from parametros import INICIADOR_LOOP

def ingresar_input(lista_opciones_posibles):
    '''Esta funcion permite que el programa no se caiga al ingresar
    algun comando'''

    print("Ingrese un comando")

    while INICIADOR_LOOP:

        comando = input()

        if comando in lista_opciones_posibles:
            return comando
        else:
            print("Comando invalido, pruebe de nuevo")
            continue


def seleccionar_jugador(entrenador):

        lista_comandos_validos = []
        for i in range(len(entrenador.equipo)):
            print("[" + str(i) + "]", entrenador.equipo[i].nombre)
            lista_comandos_validos.append(str(i))

        print()
        comando = ingresar_input(lista_comandos_validos)
        du = entrenador.equipo[int(comando)]

        return du

def seleccionar_jugador_lesionado(entrenador):

        lista_comandos_validos = []
        deportistas = []
        j = 0
        for i in range(len(entrenador.equipo)):
            if entrenador.equipo[i].lesionado == True:
                print("[" + str(j) + "]", entrenador.equipo[i].nombre)
                lista_comandos_validos.append(str(j))
                deportistas.append(entrenador.equipo[i])
                j += 1
            else:
                continue
        if lista_comandos_validos == []:
            print("No hay jugadores lesionados!")
            return False
            
        print()
        comando = ingresar_input(lista_comandos_validos)
        du = deportistas[int(comando)]
        return du


def print_estado(entrenador):
    print(entrenador.delegacion)
    print("Entrenador:", entrenador.entrenador)
    print("Moral del equipo:", round(entrenador.moral,1))
    print("Medallas:", entrenador.medallas)
    print("Dinero:", entrenador.dinero,"\n")
    print("Excelencia y respeto:", round(entrenador.excelencia_respeto, 1))
    print("Implementos deportivos:", round(entrenador.implementos_deportivos, 1))
    print("Implementos medicos:", round(entrenador.implementos_medicos, 2),"\n")
    print("Equipo Deportivo")
    print("Nombre deportista    |  Velocidad  |  Resistencia  |  Flexibilidad  |  Lesión")
    for deportista in entrenador.equipo:
        nombre = deportista.nombre
        vel = str(deportista.velocidad)
        res = str(deportista.resistencia)
        flex = str(deportista.flexibilidad)
        les = str(deportista.lesionado)
        print(f"{nombre:24.24s}{vel:18.18s}{res:17.17s}{flex:12.12s}{les}")
    

def crear_archivo():
    with open("resultados.txt", "w") as resultados:
        resultados.write("RESULTADOS DÍA A DÍA DCCUMBRE OLÍMPICA\n")
        resultados.write("--------------------------------------")

def escribir(deporte, delegacion, nombre):
    if deporte == "Ciclismo":
        with open("resultados.txt", "a") as resultados:
            resultados.write("\nCompetencia: "+ deporte+ "\n")
            resultados.write("Delegación Ganadora: " + delegacion+ "\n")
            resultados.write("Deportista Ganador: " + nombre+ "\n\n")
            resultados.write("**************************************")
        return

    with open("resultados.txt", "a") as resultados:
        resultados.write("\nCompetencia: "+ deporte+ "\n")
        resultados.write("Delegación Ganadora: " + delegacion+ "\n")
        resultados.write("Deportista Ganador: " + nombre+ "\n")
