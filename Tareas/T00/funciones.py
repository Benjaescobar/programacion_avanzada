from tablero import print_tablero
from collections import defaultdict
from parametros import NUM_BARCOS, RADIO_EXP
from bombas import bomba_cruz, bomba_regular, bomba_x, bomba_diamante
import random

#                                          -----  F  U  N  C  I  O  N  E  S   ----- 


# -----   C h e c k e a r   a p o d o   ----- 

def checkear_apodo(apodo):
    #Esta funcion tiene como fin checkear si el apodo ingresado es valido. (una extensión mínima de cinco caracteres, los que deben ser alfanuméricos)
    a = False
    while a == False:
        if len(apodo) >= 5 and apodo.isalnum():
            lista = [apodo,True]
            return lista
        else:
            print("Apodo invalido, debe tener minimo 5 caracteres y ser alfanumerico.")
            print("Pruebe de nuevo (0)")
            print("Volver al menu de inicio (1)")
            while a == False:  # Este loop debe permitir que el jugador seleccione una opcion valida sin importar cuanto se equivoque.
                eleccion = input()
                if eleccion == "0":
                    print("Ingrese apodo:")
                    apodo = input()
                    break

                elif eleccion == "1":
                    return ["",False]

                else:
                    print("Comando invalido, pruebe de nuevo")
                    continue
      
# -----   C r e a r   m a p a s   ----- 

def crear_mapas(f,c):
    mapa = []
    mapa_2 = []
    for i in range(int(f)): # con este loop se crean f listas de listas, que representan las filas del tablero
        mapa.append([])
        mapa_2.append([])
        continue
    for i in range(int(f)): # con este loop se crean c columnas vacias.
        for x in range(int(c)):
            mapa[i].append(" ")
            mapa_2[i].append(" ")
            continue
    
    mapa_computador = {"mapa visible": mapa,"mapa invisible": mapa}
    mapa = mapa_2
    a = 0
    while a < int(NUM_BARCOS): # Con este loop hacemos que el mapa que NO podemos ver del computador se le asignen aleatoriamente barcos.
        fila = int(random.randint(0, int(f)-1))
        columnas = int(random.randint(0, int(c)-1))
        if mapa_computador["mapa invisible"][fila][columnas] == " ":
            mapa_computador["mapa invisible"][fila][columnas] = "B"
            a += 1
            continue
        else:
            continue
    
    a = 0 # Esto sirve para poder empezar nuevamente el loop y definir el mapa propio

    while a < int(NUM_BARCOS): # Con este loop hacemos que el mapa de nosotros se le asignen aleatoriamente barcos.
        fila = int(random.randint(0, int(f)-1))
        columnas = int(random.randint(0, int(c)-1))
        if mapa[fila][columnas] == "B": # Este if permite que no se repita una misma posicion
            continue
        elif mapa[fila][columnas] == " ":
            mapa[fila][columnas] = "B"
            a += 1
            continue

    lista = [mapa_computador,mapa]
    
    return lista

# -----   R a n k i n g   ----- 

def ranking():
    puntajes = {}
    with open("puntajes.txt","rt") as lectura:
        leido = lectura.readlines()
        for linea in leido:
            fila = linea.strip().split(',')
            puntajes[fila[0]] = int(fila[1])


    # Ordenamiento de mayor a menor puntaje
    sort_orders = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
    rompe_loop = 0
    if len(puntajes) == 0:
        print("No hay puntajes en el ranking :/")
        return
    for i in sort_orders:
        print(i[0], i[1])
        rompe_loop += 1
        if rompe_loop >= 5:
            break
        