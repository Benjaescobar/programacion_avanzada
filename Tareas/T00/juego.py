from tablero import print_tablero
from collections import defaultdict
from parametros import NUM_BARCOS, RADIO_EXP
from bombas import bomba_cruz, bomba_regular, bomba_x, bomba_diamante
import random

def jugar(computador,jugador,columnas):

    def check_ganador(computador, jugador):

        if computador.barcos_derrivados == NUM_BARCOS:

            puntaje = len(jugador.mapa)*len(jugador.mapa[0])*NUM_BARCOS*(computador.barcos_derrivados-jugador.barcos_derrivados)
            print("Ganaste " + jugador.apodo + "!, has derrivado todos los barcos de tu enemigo","Tu puntaje fue: " + str(puntaje) + "pts"," ",sep="\n")
            retorno = ["g",puntaje]
            print_tablero(computador.mapa["mapa visible"], jugador.mapa)
            return retorno

        elif jugador.barcos_derrivados == NUM_BARCOS:
            print("Demonios, derrivaron toda tu flota " + jugador.apodo + ":(","Tu puntaje fue: 0 pts",sep="\n")
            retorno = ["p",0]
            print_tablero(computador.mapa["mapa visible"], jugador.mapa)
            return retorno

        else:
            retorno = ["no paho na","jeje"]
            return retorno


    x = True # Permite iniciar el juego
    turno = True # Asi parte jugando el usuario
    bomba_especial = True
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letra_a_numero = defaultdict(int)
    for i in range(int(columnas)): 
        # En esta parte se crea un diccionario que asocia un numero a cada valor, para luego usarlos como coordenadas.
        letra_a_numero[letras[i]] = i

    
    #                                       -----------   J U E G O   -----------
    

    while x: # x es una variable booleana que permite iniciar el loop, en este caso puntual no esta siendo usada para finalizarlo.

        chequeo = check_ganador(computador,jugador)

        if chequeo[0] == "g" or chequeo[0] == "p":
            return chequeo

        if not turno: #Este es el caso que le toca a la computadora
            fila = random.randint(0,len(jugador.mapa)-1)
            columna = random.randint(0,len(jugador.mapa[0])-1)
            if jugador.mapa[fila][columna] == " ":
                jugador.mapa[fila][columna] = "X"
                print("Tuviste suerte! el computador no le dio a ninguno de tus barcos")
                turno = True
                continue
            elif jugador.mapa[fila][columna] == "B":
                jugador.mapa[fila][columna] = "F"
                print("Ouch!, el computador le dio a uno de tus barcos!\nDisparando de nuevo...")
                jugador.barcos_derrivados += 1
                continue
            else:
                #Caso que el random sea una coordenada invalida
                continue
        
        print("-- Menu de Juego --")
        print_tablero(computador.mapa["mapa visible"], jugador.mapa) # T A B L E R O 
        print("[0] Lanzar Bomba","[1] Rendirme","[2] Salir del programa",sep="\n")
        eleccion = input()

        if eleccion == "0" and turno: #OPCION JUGAR

            print("Escoja una bomba","[0] Bomba regular","[1] Bomba especial",sep="\n")
            eleccion = input()

            if eleccion == "0": # BOMBA REGULAR
                bomba = bomba_regular(letra_a_numero,computador,jugador)
                if bomba == True:
                    computador.barcos_derrivados += 1
                    continue
                if bomba == False:
                    turno = False
                    continue

            elif eleccion == "1" and bomba_especial: # BOMBA ESPECIAL
                print("[0] Bomba Cruz","[1] Bomba X", "[2] Bomba diamante",sep="\n")
                opcion = input()
                comandos = ["0","1","2"]
                while opcion not in comandos:
                    print("Comando invalido, intentelo de nuevo")
                    opcion = input()

                if opcion == "0": # BOMBA CRUZ
                    bomba = bomba_cruz(letra_a_numero,computador,jugador)
                    bomba_especial = False
                    if bomba == 0:
                        turno = False
                        print("No derribaste ningun barco con tu bomba especial :o")
                        continue
                    else:
                        print("Derribaste",bomba,"barcos con tu bomba especial")
                        continue
                    
                
                elif opcion == "1": # BOMBA X
                    bomba = bomba_x(letra_a_numero,computador,jugador)
                    bomba_especial = False
                    if bomba == 0:
                        turno = False
                        print("No derribaste ningun barco con tu bomba especial :o")
                        continue
                    else:
                        print("Derribaste ",bomba,"barcos con tu bomba especial")
                        continue

                elif opcion == "2":
                    bomba = bomba_diamante(letra_a_numero,computador,jugador)
                    bomba_especial = False
                    if bomba == 0:
                        turno = False
                        print("No derribaste ningun barco con tu bomba especial :o")
                        continue
                    else:
                        print("Derribaste ",bomba,"barcos con tu bomba especial")
                        continue
                    pass

                

            if not bomba_especial: # bomba_especial es de caracter booleano
                print("Ya lanzaste tu unica bomba especial :/")
                continue

            else: # Comando inexistente
                print("Comando invalido, pruebe de nuevo")
                continue

        elif eleccion == "1": # Esta opcion corresponde a rendirse
            delta =(computador.barcos_derrivados-jugador.barcos_derrivados)
            puntaje = len(jugador.mapa)*len(jugador.mapa[0])*NUM_BARCOS*delta
            if puntaje < 0:
                puntaje = 0
            retorno = ["rendir",puntaje]
            return retorno

        elif eleccion == "2": # Esta opcion corresponde a salir del programa
            return "salir"

        else:
            print("Comando invalido, intente de nuevo")
            continue
