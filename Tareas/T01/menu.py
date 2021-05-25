
from parametros import INICIADOR_LOOP, DIAS_COMPETENCIA
from cargar_datos import cargar_delegaciones
from campeonato import Campeonato
from delegaciones import IEEEsparta, DCCrotona
from funciones import ingresar_input, crear_archivo, seleccionar_jugador_lesionado

##### Funciones utiles #####


def ingresar_apodo():

    # Chequea he ingresa cualquier apodo ingresado

    while INICIADOR_LOOP:
        nombre_entrenador = input()
        if nombre_entrenador.isalnum():
            return nombre_entrenador
        else:
            print("Nombre invalido :(, ingrese uno con caracteres alfanumericos")
            continue
            

###############################
########## M E N U S ##########
###############################


def menu_entrenador(entrenador, torneo):
    # M E N U   E N T R E N A D O R

    # ENTRENADOR ES EN REALIDAD UNA INSTANCIA
    # DE LA DELEGACION CORRESPONDIENTE AL USUARIO

    while INICIADOR_LOOP:

        print("[0] Fichar deportista")
        print("[1] Entrenar deportista")
        print("[2] Sanar deportista")
        print("[3] Comprar tecnologia")
        print("[4] Usar habiliidad especial")
        print("[5] Volver al menu anterior")
        print("[6] Salir del programa")

        comando = ingresar_input(["0","1","2","3","4","5","6"])

        if comando == "0":
            entrenador.fichar_deportistas(torneo)
        elif comando == "1":
            entrenador.entrenar_deportistas(torneo)
        elif comando == "2":
            torneo.entrenador.sanar_lesiones(torneo)
        elif comando == "3":
            entrenador.comprar_tecnologia(torneo)
        elif comando == "4":
            entrenador.habilidad_especial(torneo)
        elif comando == "5":
            return True
        else:
            return False

##### COMPETENCIA #####

def menu_competencia(torneo):

    pass

##### MENU PRINCIPAL #####

def menu_principal(entrenador, torneo):

    #  Esta variable el proposito de iniciar los while de cada menu.
    

    while INICIADOR_LOOP:
        print(torneo.dia_actual)
        print(DIAS_COMPETENCIA)
        if torneo.dia_actual >= DIAS_COMPETENCIA:
            print("\nSE ACABO LA COMPETENCIA! -O-\n")
            with open("resultados.txt", "r") as resultados:
                for row in resultados:
                    print(row)

            # torneo.mostrar_estado()
            if torneo.medallero["IEEEsparta"] > torneo.medallero["DCCrotona"]:
                print("\nFelicitaciones a", torneo.entrenador.delegacion, "por su victoria\n")
            elif torneo.medallero["IEEEsparta"] < torneo.medallero["DCCrotona"]:
                print("\nFelicitaciones a", torneo.rival.delegacion, "por su victoria\n")
            else:
                print("NO GANO NADIEEEEEEE\n")
            return
        if torneo.dia_actual % 2 != 0:
            imprimir = "y te toca entrenar, aprovecha de hacer mejoras utiles\n"
            print("\nEstas en el dia",torneo.dia_actual,imprimir)
        print("[0] Menu entrenador")
        print("[1] Simular competencias")
        print("[2] Mostrar estado competencia")
        print("[3] Salir del programa")

        # ingresar_input es una funcion que corrobora que el comando ingresado es valido

        comando = ingresar_input(["0","1","2","3"])

        if comando == "0":
            menu = menu_entrenador(entrenador,torneo)
            # menu_entrenador retorna False para salir del programa
            if menu:
                continue
            else:
                print("Adios")
                return
        
        elif comando == "1":
            # ACA VA LA COMPETENCIA
            torneo.dia_actual += 1
            torneo.competencias()
            torneo.dia_actual +=1
            pass

        elif comando == "2":
            # estado competencia
            torneo.mostrar_estado()
        
        else:
            return


##### MENU INICIADOR JUEGO #####

def menu_inicio():
    while INICIADOR_LOOP:
        print("[0] Iniciar juego\n[1] Salir del programa")
        comando = ingresar_input(["0","1"])

        if comando == "0":
            crear_archivo()
            # SE INICIA EL JUEGO
            print("Ingrese su nombre:")
            nombre_entrenador = ingresar_apodo()
            print("Ingrese el nombre de su rival:")
            nombre_rival = ingresar_apodo()

            print("Escoja una delegacion")
            print("[0] IEEEsparta\n[1] DCCrotona")

            comando = ingresar_input(["0","1"])

            if comando == "0":
                # delegaciones retorna un diccionario

                datos_esparta = cargar_delegaciones()["IEEEsparta"]
                datos_crotona = cargar_delegaciones()["DCCrotona"]

                entrenador = IEEEsparta(nombre_entrenador,datos_esparta[0],datos_esparta[1],datos_esparta[2],datos_esparta[3])
                rival = DCCrotona(nombre_rival,datos_crotona[0],datos_crotona[1],datos_crotona[2],datos_crotona[3])
                
                torneo = Campeonato(entrenador,rival)
                menu_principal(entrenador,torneo)

            elif comando == "1":
                datos_esparta = cargar_delegaciones()["IEEEsparta"]
                datos_crotona = cargar_delegaciones()["DCCrotona"]

                rival = IEEEsparta(nombre_rival, datos_esparta[0], datos_esparta[1], datos_esparta[2], datos_esparta[3])
                entrenador = DCCrotona(nombre_entrenador, datos_crotona[0], datos_crotona[1], datos_crotona[2], datos_crotona[3])
                
                torneo = Campeonato(entrenador,rival)
                menu_principal(entrenador,torneo)

        else:
            return
