from parametros import NUM_BARCOS, RADIO_EXP

def pedir_coordenadas(letra_a_numero,jugador,computador):
    print("Selecciona unas coordenadas")
    print("Letra y Numero (e.x. a,1)")
    x = True
    permitidos_numeros = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]
    while x:
        coordenadas = input()
        coordenadas = coordenadas.split(",")
        if coordenadas[0].upper() in letra_a_numero and coordenadas[1] in permitidos_numeros:
            if int(coordenadas[1]) < len(jugador.mapa):
                letra = coordenadas[0].upper()
                num = coordenadas[1]
                lista = [letra,num]
                return lista
            else:
                print("Coordenada invalida, intentelo de nuevo (e.x. a,1)")
                continue
        else:
            print("Coordenada invalida, intentelo de nuevo (e.x. a,1)")
            continue

def bomba_regular(letra_a_numero,computador,jugador):
    coordenadas = pedir_coordenadas(letra_a_numero,jugador,computador)
    letra = coordenadas[0]
    num = coordenadas[1]
            

    # el  ' mapa invisible ' es el que contiene la informacion de la ubicacion de los barcos, el visible es el que podemos ver.
    if computador.mapa["mapa invisible"][int(num)][int(letra_a_numero[letra])] == " ": 
        computador.mapa["mapa visible"][int(num)][int(letra_a_numero[letra])] = "X"
        print("No había un barco en esa posición :/, le toca a la computadora.","",sep="\n")
        return False
    elif computador.mapa["mapa invisible"][int(num)][int(letra_a_numero[letra])] == "B":
        computador.mapa["mapa visible"][int(num)][int(letra_a_numero[letra])] = "F"
        print("")
        print("Derrotaste el barco ubicado en",letra+str(num),"! tienes otro intento :O")
        return True

    else:
        print("Ya lanzaste a esa coordenada...\n")
        return True

def bomba_cruz(letra_a_numero,computador,jugador):
    x = True
    barcos_derrivados_bomba = 0
    coordenadas = pedir_coordenadas(letra_a_numero,jugador,computador)
    letra = coordenadas[0]
    num = coordenadas[1]
    
    for i in range(RADIO_EXP): # BOMBA
        fila = int(num)
        columnas = letra_a_numero[letra]
        if x:
            # Parte vertical cruz
            if fila + i < len(jugador.mapa):
                if computador.mapa["mapa invisible"][fila + i][columnas] == " ":
                    computador.mapa["mapa visible"][fila + i][columnas] = "X"

                elif computador.mapa["mapa invisible"][fila + i][columnas] == "B":
                    computador.mapa["mapa visible"][fila + i][columnas] = "F"
                    computador.barcos_derrivados += 1 # Esto es para el conteo final
                    barcos_derrivados_bomba += 1 # Esto es para saber cuantos barcos derrivo la bomba especial
                else:
                    pass

            if fila - i >= 0:
                if computador.mapa["mapa invisible"][fila - i][columnas] == " ":
                    computador.mapa["mapa visible"][fila - i][columnas] = "X"

                elif computador.mapa["mapa invisible"][fila - i][columnas] == "B":
                    computador.mapa["mapa visible"][fila - i][columnas] = "F"
                    computador.barcos_derrivados += 1
                    barcos_derrivados_bomba += 1
                else:
                    pass

        if x:
            # Parte horizontal cruz
            if columnas + i < len(jugador.mapa[0]):
                if computador.mapa["mapa invisible"][fila][columnas + i] == " ":
                    computador.mapa["mapa visible"][fila][columnas + i] = "X"

                if computador.mapa["mapa invisible"][fila][columnas + i] == "B":
                    computador.mapa["mapa visible"][fila][columnas + i] = "F"
                    computador.barcos_derrivados += 1
                    barcos_derrivados_bomba += 1
                else:
                    pass

            if columnas - i >= 0:
                if computador.mapa["mapa invisible"][fila][columnas - i] == " ":
                    computador.mapa["mapa visible"][fila][columnas  - i] = "X"

                if computador.mapa["mapa invisible"][fila][columnas - i] == "B":
                    computador.mapa["mapa visible"][fila][columnas - i] = "F"

                    computador.barcos_derrivados += 1
                    barcos_derrivados_bomba += 1
                else:
                    pass

        continue

    return barcos_derrivados_bomba

def bomba_x(letra_a_numero,computador,jugador): 
    x = True
    barcos_derrivados_bomba = 0
    coordenadas = pedir_coordenadas(letra_a_numero,jugador,computador)
    letra = coordenadas[0]
    num = coordenadas[1]

    for i in range(RADIO_EXP): # BOMBA
        fila = int(num)
        columnas = letra_a_numero[letra]
        if x:
            if fila + i < len(jugador.mapa) and columnas + i < len(jugador.mapa[0]):
                if computador.mapa["mapa invisible"][fila + i][columnas + i] == " ":
                    computador.mapa["mapa visible"][fila + i][columnas + i] = "X"

                elif computador.mapa["mapa invisible"][fila + i][columnas + i] == "B":
                    computador.mapa["mapa visible"][fila + i][columnas + i] = "F"
                    computador.barcos_derrivados += 1 # Esto es para el conteo final
                    barcos_derrivados_bomba += 1 # Esto es para saber cuantos barcos derrivo la bomba especial
                else:
                    pass

            if fila - i >= 0 and columnas - i >= 0: #
                if computador.mapa["mapa invisible"][fila - i][columnas - i] == " ":
                    computador.mapa["mapa visible"][fila - i][columnas - i] = "X"

                elif computador.mapa["mapa invisible"][fila - i][columnas - i] == "B":
                    computador.mapa["mapa visible"][fila - i][columnas - i] = "F"
                    computador.barcos_derrivados += 1
                    barcos_derrivados_bomba += 1
                else:
                    pass
            
            if fila + i < len(jugador.mapa) and columnas - i >= 0: # Izquierda abajo
                if computador.mapa["mapa invisible"][fila + i][columnas - i] == " ":
                    computador.mapa["mapa visible"][fila + i][columnas - i] = "X"

                elif computador.mapa["mapa invisible"][fila - i][columnas - i] == "B":
                    computador.mapa["mapa visible"][fila + i][columnas - i] = "F"
                    computador.barcos_derrivados += 1
                    barcos_derrivados_bomba += 1
                else:
                    pass
            
            if fila - i >= 0 and columnas + i < len(jugador.mapa[0]): # Derecha abajo
                if computador.mapa["mapa invisible"][fila - i][columnas + i] == " ":
                    computador.mapa["mapa visible"][fila - i][columnas + i] = "X"

                elif computador.mapa["mapa invisible"][fila - i][columnas + i] == "B":
                    computador.mapa["mapa visible"][fila - i][columnas + i] = "F"
                    computador.barcos_derrivados += 1
                    barcos_derrivados_bomba += 1
                else:
                    pass

        continue

    return barcos_derrivados_bomba

def bomba_diamante(letra_a_numero,computador,jugador):
    x = True
    barcos_derrivados_bomba = 0
    def cuerpo_diamante(t,fila,columnas):
        barcos_derrivados_bomba = 0
        for x in range(t):
            if columnas + x < len(jugador.mapa[0]):
                if computador.mapa["mapa invisible"][fila][columnas + x] == " ":
                    computador.mapa["mapa visible"][fila][columnas + x] = "X"

                if computador.mapa["mapa invisible"][fila][columnas + x] == "B":
                    computador.mapa["mapa visible"][fila][columnas + x] = "F"
                    computador.barcos_derrivados += 1
                    barcos_derrivados_bomba += 1
                else:
                    pass
            if columnas - x >= 0:
                if computador.mapa["mapa invisible"][fila][columnas - x] == " ":
                    computador.mapa["mapa visible"][fila][columnas  - x] = "X"

                if computador.mapa["mapa invisible"][fila][columnas - x] == "B":
                    computador.mapa["mapa visible"][fila][columnas - x] = "F"
                    computador.barcos_derrivados += 1
                    barcos_derrivados_bomba += 1
                else:
                    pass
        return barcos_derrivados_bomba
            

    coordenadas = pedir_coordenadas(letra_a_numero,jugador,computador)
    letra = coordenadas[0]
    num = coordenadas[1]

    for i in range(RADIO_EXP): # BOMBA
        fila = int(num)
        columnas = letra_a_numero[letra]
        t = RADIO_EXP - i
        
        if x: # Parte vertical diamante
            
            if fila + i < len(jugador.mapa):
                if computador.mapa["mapa invisible"][fila + i][columnas] == " ":
                    computador.mapa["mapa visible"][fila + i][columnas] = "X"
                    barcos_derrivados_bomba += cuerpo_diamante(t,fila + i,columnas)
                    
                elif computador.mapa["mapa invisible"][fila + i][columnas] == "B":
                    computador.mapa["mapa visible"][fila + i][columnas] = "F"
                    barcos_derrivados_bomba += 1 # Esto es para saber cuantos barcos derrivo la bomba especial
                    barcos_derrivados_bomba += cuerpo_diamante(t,fila + i,columnas)
                    computador.barcos_derrivados += 1 # Esto es para el conteo final
                else:
                    pass

            if fila - i >= 0:

                if computador.mapa["mapa invisible"][fila - i][columnas] == " ":
                    computador.mapa["mapa visible"][fila - i][columnas] = "X"
                    barcos_derrivados_bomba += cuerpo_diamante(t,fila - i,columnas)

                elif computador.mapa["mapa invisible"][fila - i][columnas] == "B":
                    computador.mapa["mapa visible"][fila - i][columnas] = "F"
                    barcos_derrivados_bomba += cuerpo_diamante(t,fila - i,columnas)
                    computador.barcos_derrivados += 1
                    barcos_derrivados_bomba += 1
                    
                else:
                    pass
       
        continue

    return barcos_derrivados_bomba