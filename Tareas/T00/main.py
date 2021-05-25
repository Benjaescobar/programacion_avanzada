from funciones import checkear_apodo, crear_mapas, ranking
from juego import jugar

x = True

class Jugador:
    
    def __init__(self,apodo,mapa):
        self.apodo = apodo
        self.mapa = mapa
        self.barcos_derrivados = 0

while x: # Este while corresponde al funcionamiento del programa

    print(" ","-- Menu de inicio --","","¿Que desea hacer?","[0] Iniciar partida","[1] Ver Ranking de puntajes","[2] Salir del programa",sep="\n")

    a = 0

    while a != 2: # Este while corresponde a cualquier opcion que no sea el menu de inicio.
        a = input()

        if a == "0":  # En este caso se inicia la partida

            # Partida:
            print("Ingrese un apodo:")
            apodo = input()
            check = checkear_apodo(apodo)
            if check[1]: # check[1] es un bool, en este caso el juego se ejecuta ya que el apodo esta correcto
                apodo = check[0]
                print("Ingrese Las dimensiones del tablero, primero las filas, y luego las columnas.")
                while x: # Ingreso de Filas y columnas, es un loop para prevenir el caso en que se equivoque en poner los numeros.
                    print("Filas:")
                    f = input()
                    permitidos = "3456789101112131415"
                    if f not in permitidos:  # Para prevenir el caso de que no se ponga el comando valido
                        print("Ingrese un numero valido")
                        continue
                    if int(f) < 3 or int(f) > 15:
                        print("El tablero debe tener entre 3 y 15 filas, ingrese nuevamente")
                        continue
                    break
                while x:
                    print("Columnas:")
                    c = input()
                    permitidos = "3456789101112131415"
                    if c not in permitidos:
                        print("Ingrese un numero valido")
                        continue
                    if int(c) < 3 or int(c) > 15:
                        print("El tablero debe tener entre 3 y 15 columnas, ingrese nuevamente")
                        continue
                    
                    break

                mapa = crear_mapas(f,c)

                computador = Jugador("computador",mapa[0])
                usuario = Jugador(apodo,mapa[1])
                
                juego = jugar(computador,usuario,c) # el mapa[0] corresponde al mapa del computador

                if juego[0] == "g":
                    
                    with open("puntajes.txt","a") as guardar:
                        texto = "\n" + apodo + "," + str(juego[1])
                        guardar.write(texto)
                        guardar.close()
                    a = 2

                if juego[0] == "p":
                    a = 2

                if juego[0] == "rendir":
                    with open("puntajes.txt","a") as guardar:
                        texto = "\n" + apodo + "," + str(juego[1])
                        guardar.write(texto)
                        guardar.close()
                    print("Te has rendido! de todas formas tu puntaje fue", juego[1])
                    a = 2

                elif juego == "salir":
                    x = False
                    a = 2

            else:    # Si check no era True, se vuelve al menu de inicio.
                break

        elif a == "1": # En este caso se presenta el Top Ranking del momento.
            print("-- Ranking puntajes -- \n")
            ranking()
            print("","[0] volver al inicio", "[1] Cerrar programas",sep="\n")
            while x: # Loop por si se equivoca
                opcion = input()
                if opcion == "0":
                    a = 2
                    break
                elif opcion == "1":
                    x = False
                    a = 2
                    continue
                else:
                    print("comando invalido")
                    continue

        elif a == "2":  # En este caso se cierra el programa.
            print("Adios")
            x = False
            break

        else:  # Este es en caso de que se equivoque en ingresar un comando.
            print("Comando invalido, intentelo de nuevo")
            continue
