from deporte import Atletismo, Natacion, Gimnasia, Ciclismo, Deportes
from random import randint
from funciones import ingresar_input, print_estado, escribir
from parametros import DIAS_COMPETENCIA, BONIFICACION_DCC

class Campeonato():

    def __init__(self,entrenador,rival):


        self.entrenador = entrenador
        self.rival = rival
        self.dia_actual = 1
        self.medallero = {
            "IEEEsparta": 0,
            "DCCrotona": 0
        }
        self.medallero_cada_competencia = {
            "Atletismo": {"IEEEsparta": 0, "DCCrotona": 0},
            "Natacion": {"IEEEsparta": 0, "DCCrotona": 0},
            "Gimnasia": {"IEEEsparta": 0, "DCCrotona": 0},
            "Ciclismo": {"IEEEsparta": 0, "DCCrotona": 0}
        }

    def seleccionar_jugador(self):

        lista_comandos_validos = []
        for i in range(len(self.entrenador.equipo)):
            print("[" + str(i) + "]", self.entrenador.equipo[i].nombre)
            lista_comandos_validos.append(str(i))

        print()
        comando = ingresar_input(lista_comandos_validos)
        du = self.entrenador.equipo[int(comando)]

        return du

    def competencias(self):

        #### du = deportista usuario  #### 
        #### dr = deportista rival    ####
        # Selecciona el deportista
        entrenador = self.entrenador
        rival = self.rival
        # ATLETISMO

        print("\nEscoja uno de los siguientes deportistas para Atletismo\n")
        du = self.seleccionar_jugador()
        # Se escoje alatoriamente el deportista del rival
        dr = self.rival.equipo[randint(0,len(self.rival.equipo)-1)]
        # Se calcula el ganador de la competencia correspondiente
        resultado_atletismo = Atletismo.calcular_ganador(self, du, dr, entrenador, rival) 

        # Las siguientes lineas se repite esto para cada competencia

        # NATACION
        print("\nEscoja uno de los siguientes deportistas para Natacion\n")
        du = self.seleccionar_jugador()
        dr = self.rival.equipo[randint(0,len(self.rival.equipo)-1)]
        
        resultado_natacion = Natacion.calcular_ganador(self, du, dr, entrenador, rival) 

        # Gimnasia
        print("\nEscoja uno de los siguientes deportistas para Gimnasia\n")
        du = self.seleccionar_jugador()
        dr = self.rival.equipo[randint(0,len(self.rival.equipo)-1)]
        resultado_gimnasia = Gimnasia.calcular_ganador(self, du, dr, entrenador, rival) 

        # Ciclismo
        print("\nEscoja uno de los siguientes deportistas para Ciclismo\n")
        du = self.seleccionar_jugador()
        dr = self.rival.equipo[randint(0,len(self.rival.equipo)-1)]

        resultado_ciclismo = Ciclismo.calcular_ganador(self, du, dr, entrenador, rival) 

        resultados = [resultado_atletismo,resultado_natacion,resultado_gimnasia,resultado_ciclismo]

        self.premiar(resultados)
        

        
    def premiar(self, resultados):
        '''
        Breve explicacion:
            resultados es una lista de listas que contiene
            quien gano cada deporte, y ambos competidores de este,
            de esa forma se puede premiar y "castigar" a cada jugador.
        '''
        # Loop para hacer mas eficiente los cambios
        with open("resultados.txt", "a") as result:
            result.write("\nDia: " + str(self.dia_actual) + "\n")

        for i in range(len(resultados)):
            # Bonificaciones

            ### ENCUENTRA EL JUGADOR EN EL TEAM
            for jugador in self.entrenador.equipo:
                if resultados[i][1].nombre == jugador.nombre:
                    dep_usuario = jugador
                else:
                    pass
            for jugador in self.rival.equipo:
                if resultados[i][2].nombre == jugador.nombre:
                    dep_rival = jugador
                else:
                    pass
            
            if resultados[i][0] == "deportista usuario":
                deporte = resultados[i][3]
                delegacion = self.entrenador.delegacion
                nombre = resultados[i][1].nombre
                escribir(deporte, delegacion , nombre)

                # Caso en que gane el usuario
                if delegacion == "DCCrotona":
                    self.entrenador.dinero += 100
                    dep_usuario.moral += 20 * BONIFICACION_DCC
                    dep_rival.moral -= 20
                    self.rival.excelencia_respeto -= 0.02
                    self.medallero[delegacion] += 1
                    self.medallero_cada_competencia[deporte][delegacion] += 1
                else:
                    self.entrenador.dinero += 100
                    dep_usuario.moral += 20
                    dep_rival.moral -= 10
                    self.rival.excelencia_respeto -= 0.02
                    self.medallero[delegacion] += 1
                    self.medallero_cada_competencia[deporte][delegacion] += 1
                
                imprimir_1 = "Felicitaciones a la delegacion " + delegacion
                imprimir_2 = " por su merecida victoria en " + deporte
                print(imprimir_1 + imprimir_2)
                
            elif resultados[i][0] == "deportista rival":
                deporte = resultados[i][3]
                delegacion = self.rival.delegacion
                nombre = resultados[i][2].nombre
                escribir(deporte, delegacion , nombre)
                # Caso en que gane el computador
                if delegacion == "DCCrotona":
                    self.rival.dinero += 100
                    dep_rival.moral += 20 * BONIFICACION_DCC
                    dep_usuario.moral -= 20
                    self.entrenador.excelencia_respeto -= 0.02
                    self.medallero[delegacion] += 1
                    self.medallero_cada_competencia[deporte][delegacion] += 1
                else:
                    self.rival.dinero += 100
                    dep_rival.moral += 20
                    dep_usuario.moral -= 10
                    self.entrenador.excelencia_respeto -= 0.02
                    self.medallero[delegacion] += 1
                    self.medallero_cada_competencia[deporte][delegacion] += 1
                
                imprimir_1 = "Felicitaciones a la delegacion " + self.rival.delegacion
                imprimir_2 = " por su merecida victoria en " + resultados[i][3]
                print(imprimir_1 + imprimir_2)

            else:
                deporte = resultados[i][3]
                delegacion = self.rival.delegacion
                escribir(deporte, "Empate" , "-")
                print("Wow, hubo un empate en " + resultados[i][3])

        self.calcular_moral()
        
    def calcular_moral(self):

        promedio_moral_usuario = 0
        for jugador in self.entrenador.equipo:
            promedio_moral_usuario += jugador.moral

        promedio_moral_usuario = max(0,min(100,int(promedio_moral_usuario//len(self.entrenador.equipo))))

        self.entrenador.moral = promedio_moral_usuario

        promedio_moral_rival = 0
        for jugador in self.rival.equipo:
            promedio_moral_rival += jugador.moral

        promedio_moral_rival = max(0,min(100,int(promedio_moral_rival//len(self.rival.equipo))))

        self.rival.moral = promedio_moral_rival
        


    def mostrar_estado(self):
        print()
        print("                      ESTADO DE LAS DELEGACIONES Y DEPORTISTAS                     ")
        print("-----------------------------------------------------------------------------------")
        print_estado(self.entrenador)
        print("***********************************************************************************")
        print_estado(self.rival)
        print("-----------------------------------------------------------------------------------")
        if self.dia_actual % 2 == 0:
            print("Dia",self.dia_actual,": Entrenamiento\n")
        else:
            print("Dia",self.dia_actual,": Competencia\n")

        print("Medallero")
        print("Deporte     |   IEEEsparta   |   DCCrotona")
        deportes = self.medallero_cada_competencia
        for medalla in self.medallero_cada_competencia:
            iee = str(deportes[medalla]['IEEEsparta'])
            dcc = str(deportes[medalla]['DCCrotona'])
            print(f"{medalla:20.20}{iee:16.16}{dcc}")
