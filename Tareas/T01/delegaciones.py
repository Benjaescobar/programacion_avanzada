from parametros import INICIADOR_LOOP
import parametros as p
from abc import ABC, abstractmethod
from random import uniform, randint
from cargar_datos import cargar_deportistas
from funciones import ingresar_input, seleccionar_jugador, seleccionar_jugador_lesionado

class Delegaciones(ABC):

    def __init__(self,entrenador,equipo,medallas,moral,dinero):
        # Atributos entregados
        self.entrenador = entrenador
        self.equipo = equipo
        self.medallas = medallas
        self.moral = moral
        self.dinero = dinero
        
        # Atributos generados
        
        self.__excelencia_respeto = uniform(0,1)
        self.implementos_deportivos = uniform(0,1)
        self.implementos_medicos = uniform(0,1)

    @property
    def excelencia_respeto(self):
        return self.__excelencia_respeto

    @excelencia_respeto.setter
    def excelencia_respeto(self, parametros):
        # Este setter tiene la funcion de que
        # se mantengan los limites
        if self.excelencia_respeto < 0.0:
            self.excelencia_respeto = 0.0
        
        elif self.excelencia_respeto > 1.0:
            self.excelencia_respeto = 1.0
        else:
            pass

    def fichar_deportistas(self,torneo):
        if self.moral > p.MORAL_MINIMA:
            lista_comandos_validos = []
            deportistas = cargar_deportistas()
            nombres_deportistas = list(deportistas.keys())
            jugadores_fichados = []
            deportistas_fichables = []
            for jugador in self.equipo:
                jugadores_fichados.append(jugador.nombre)

            for jugador in torneo.rival.equipo:
                jugadores_fichados.append(jugador.nombre)
            # Aqui se imprimen los deportistas disponibles
            for i in range(len(nombres_deportistas)):
                if nombres_deportistas[i] in jugadores_fichados:
                    continue
                else:
                    nom = nombres_deportistas[i]
                    print("[" + str(len(deportistas_fichables)) + "]", nom)
                    lista_comandos_validos.append(str(len(deportistas_fichables)))
                    deportistas_fichables.append(nombres_deportistas[i])
            print()
            while INICIADOR_LOOP:
                comando = int(ingresar_input(lista_comandos_validos))
                print("Fichaste al deportista",deportistas_fichables[int(comando)])
                print()
                self.equipo.append(deportistas[deportistas_fichables[int(comando)]])
                return

            # FALTA QUE SE CHEQUEE QUE EL JUGADOR NO ESTA FICHADO
        else:
            print("Lamentablemente la moral de tu equipo esta muy baja :/")
            pass

    def entrenar_deportistas(self, torneo, ponderador):
        if self.dinero < p.COSTO_ENTRENAR:
            print("No tienes suficiente dinero")
            return
        else:
            print("\nEscoja un jugador para entrenar:\n")
            deportista = seleccionar_jugador(torneo.entrenador)
            print("\nEscoja un atributo a mejorar\n")
            self.dinero -= p.COSTO_ENTRENAR
            for i in range(len(torneo.entrenador.equipo)):
                ds = torneo.entrenador.equipo[i]
                if ds.nombre == deportista.nombre:
                    ds.entrenar(torneo, ponderador)
                    break
                    
    def sanar_lesiones(self, torneo):
        print("Seleccione uno de los siguientes jugadores para sanarlo:")
        du = seleccionar_jugador_lesionado(torneo.entrenador)
        
        if du == False:
            print("\nSera po..., gasta las moneas en otra cosa\n")
            return True
        print(du.nombre)
        for i in range(len(torneo.entrenador.equipo)):
            if du.nombre == torneo.entrenador.equipo[i].nombre:
                posicion = i
        deportista = torneo.entrenador.equipo[posicion]
        if torneo.entrenador.dinero >= 30:
            torneo.entrenador.dinero -= 30
            md = deportista.moral
            im = torneo.entrenador.implementos_medicos
            er = torneo.entrenador.excelencia_respeto
            probabilidad_sanar = min(1, max(0,(md * (im + er))/200))

            if uniform(0,1) < probabilidad_sanar:
                print("\nTu deportista ha sido sanado! :DDD\n")
                torneo.entrenador.equipo[posicion].lesionado = False
                return
            else:
                print("\nTu deportista no se ha podido sanar -_-, quizas esta muy triste\n")
                retorno = "NADA"
                return retorno
        else:
            principio_mensaje = "No te alcanza para sanar a tu jugador, tienes"
            final_mensaje = "DCCoins, necesitas 30"
            print(principio_mensaje, self.dinero, final_mensaje)
            retorno = "NADA"
            return retorno

    def comprar_tecnologia(self, torneo):
        if torneo.entrenador.dinero >= 20:
            torneo.entrenador.dinero -= 20
            ide = torneo.entrenador.implementos_deportivos
            im = torneo.entrenador.implementos_medicos
            print("Tu tecnologia actual es:")
            print("Implementos deportivos:", torneo.entrenador.implementos_deportivos)
            print("Implementos medicos:",torneo.entrenador.implementos_medicos)
            print("\nMejorando...\n")
            torneo.entrenador.implementos_deportivos = round(min(1,ide*1.1),2)
            torneo.entrenador.implementos_medicos = round(min(1,im*1.1),2)
            print("MEJORADOOOO :D\n")
            #u_id = torneo.entrenador.implementos_deportivos
            #u_im = torneo.entrenador.implementos_medicos
            ide = torneo.entrenador.implementos_deportivos
            im = torneo.entrenador.implementos_medicos
            print("nuevo nivel Implementos deportivos:", ide)
            print("nuevo nivel Implementos medicos:", im, "\n")
            return
        else:
            print("No tienes suficiente dinero :(")
            print("Dinero:",torneo.entrenador.dinero,"\n")
            return


    # Este metodo es abstracto porque cada delegacion tiene una hablidad distinta
    @abstractmethod
    def habilidad_especial(self):
        pass

class IEEEsparta(Delegaciones):

    def __init__(self,entrenador,equipo,medallas,moral,dinero):
        super().__init__(entrenador,equipo,medallas,moral,dinero)

        self.delegacion = "IEEEsparta"
        self.excelencia_respeto = uniform(0.4,0.8)
        self.implementos_deportivos = uniform(0.3,0.7)
        self.implementos_medicos = uniform(0.2,0.6)
        self.oportunidad = 1


    def fichar_deportistas(self, torneo):
        super().fichar_deportistas(torneo)

    def entrenar_deportistas(self, torneo):
        super().entrenar_deportistas(torneo, p.BONIFICACION_IEE)
        return

    def sanar_lesiones(self, torneo):
        super().sanar_lesiones(torneo)

    def comprar_tecnologia(self, torneo):
        super().comprar_tecnologia(torneo)

    def habilidad_especial(self, torneo):
        # Oportunidad corresponde
        oportunidad = torneo.entrenador.oportunidad
        if torneo.entrenador.dinero > 20 and oportunidad == 1:
            print("\nTHIS. IS. SPARTAAAA\n")
            for deportista in torneo.entrenador.equipo:
                deportista.moral = 100
            torneo.entrenador.oportunidad -= 1
        else:
            print("\nYa usaste tu poder...\n")


class DCCrotona(Delegaciones):

    def __init__(self,entrenador,equipo,medallas,moral,dinero):
        super().__init__(entrenador,equipo,medallas,moral,dinero)

        self.delegacion = "DCCrotona"

        self.oportunidad = 1
        self.excelencia_respeto = uniform(0.4,0.8)
        self.implementos_deportivos = uniform(0.2,0.6)
        self.implementos_medicos = uniform(0.4,0.8)

    def fichar_deportistas(self, torneo):
        super().fichar_deportistas(torneo)

    def entrenar_deportistas(self, torneo):
        super().entrenar_deportistas(torneo, 1)
        return

    def sanar_lesiones(self, torneo):
        super().sanar_lesiones(torneo)

    def comprar_tecnologia(self, torneo):
        super().comprar_tecnologia(torneo)

    def habilidad_especial(self, torneo):
        oportunidad = torneo.entrenador.oportunidad
        if torneo.entrenador.dinero > 20 and oportunidad == 1:
            print("\nMedallita gratuita\n")
            torneo.entrenador.dinero += 100
            nueva_moral = float(torneo.entrenador.moral + 20)
            torneo.entrenador.moral = max(0,min(nueva_moral,100))
            torneo.rival.excelencia_respeto -= 0.02
            torneo.medallero[torneo.entrenador.delegacion] += 1
            torneo.entrenador.medallas += 1
            torneo.entrenador.oportunidad -= 1
        else:
            print("\nYa usaste tu poder...\n")
            pass