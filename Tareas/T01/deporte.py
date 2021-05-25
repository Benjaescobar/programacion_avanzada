from abc import ABC,abstractmethod
import parametros as p
from funciones import ingresar_input
from random import uniform

class Deportistas():

    def __init__(self, nom, vel, res, flex, mor, les, pr):
        self.nombre = nom
        self.__velocidad = vel
        self.__resistencia = res
        self.__flexibilidad = flex
        self.__moral = mor
        self.lesionado = les
        self.precio = pr

    @property
    def velocidad(self):
        return self.__velocidad
    
    @velocidad.setter
    def velocidad(self, parametros):
        if self.__velocidad < 0:
            self.__velocidad = 0
        if self.__velocidad > 100:
            self.__velocidad = 100

    @property
    def resistencia(self):
        return self.__resistencia
    
    @resistencia.setter
    def resistencia(self, parametros):
        if self.__resistencia < 0:
            self.__resistencia = 0
        if self.__resistencia > 100:
            self.__resistencia = 100
    
    @property
    def flexibilidad(self):
        return self.__flexibilidad
    
    @flexibilidad.setter
    def flexibilidad(self, parametros):
        if self.__flexibilidad < 0:
            self.__flexibilidad = 0
        if self.__flexibilidad > 100:
            self.__flexibilidad = 100

    @property
    def moral(self):
        return self.__moral
    
    @moral.setter
    def moral(self, parametros):
        if self.__moral < 0:
            self.__moral = 0
        if self.__moral > 100.0:
            self.__moral = 100.0
    

    def entrenar(self, torneo, ponderador):
        print("[0] Velocidad\n[1] Resistencia\n[2] Flexibilidad")
        comando = ingresar_input(["0","1","2"])
        
        if comando == "0":
            minimum = self.__velocidad + int(p.PUNTOS_ENTRENAMIENTO)*ponderador
            self.__velocidad = int(min(100,minimum))
            print("\nLa nueva velocidad de",self.nombre,"es",self.__velocidad)
            print()
        elif comando == "1":
            minimum = self.__resistencia + p.PUNTOS_ENTRENAMIENTO*ponderador
            self.__resistencia = int(min(100,minimum))
            print("\nLa nueva resistencia de",self.nombre,"es",self.__resistencia)
            print()
        else:
            minimum = self.__flexibilidad + p.PUNTOS_ENTRENAMIENTO*ponderador
            self.__flexibilidad = int(min(100,minimum))
            print("\nLa nueva flexibilidad de",self.nombre,"es",self.__flexibilidad)
            print()

    def lesionarse(self, riesgo, delegacion):
        loteria = uniform(0,1)
        if loteria < riesgo:
            print("Ouchhhh!!!", self.nombre,"de",delegacion.delegacion, "se lesiono!")
            self.lesionado = True
        else:
            return

class Deportes(ABC):

    def __init__(self, implementos, riesgo, deporte):
        self.implementos = implementos
        self.riesgo = riesgo
        self.deporte = deporte


    def validacion_competencia(self,du,dr, entrenador, rival, deporte):

        gana_entrenador = ["deportista usuario", du, dr, deporte]
        gana_rival = ["deportista rival", du, dr, deporte]
        
        if dr.lesionado == True and du.lesionado == True:
            return ["Empate", du, dr, deporte]
        

        elif du.lesionado == True:
            print("usuario lesionado")
            return gana_rival
        elif dr.lesionado == True:
            print("rival lesionado")
            return gana_entrenador

        if deporte != "Atletismo":
            entrenador = entrenador.implementos_deportivos
            rival = rival.implementos_deportivos 
            if entrenador > p.NIVEL_IMPLEMENTOS and rival > p.NIVEL_IMPLEMENTOS:
                return True
            else:
                if entrenador < p.NIVEL_IMPLEMENTOS and rival > p.NIVEL_IMPLEMENTOS:
                    return gana_rival
                elif rival < p.NIVEL_IMPLEMENTOS and entrenador > p.NIVEL_IMPLEMENTOS:
                    return gana_entrenador
                else:
                    return ["Empate", du, dr, deporte]
        else:
            return True

    @abstractmethod
    def calcular_ganador(self, du, dr):
        pass

#######################################
##### CLASES HEREDADAS DE DEPORTE #####
#######################################

class Atletismo(Deportes):

    def __init__(self):
        super().__init__(False, 0.2, "Atletismo")

    def validacion_competencia(self, du, dr, entrenador, rival,deporte):
        retorno = Deportes.validacion_competencia(self,du, dr, entrenador, rival, deporte)
        return retorno

    def calcular_ganador(self, du, dr, entrenador, rival):
        #### du = deportista usuario ####
        #### dr = deportista rival ####

        # La funcion lesionarse te lesiona con la probabilidad que se nos entrega
        # Ver la en la clase Deportistas (linea 6)
        du.lesionarse(0.2, entrenador)
        dr.lesionarse(0.2, rival)

        validacion = Atletismo.validacion_competencia(self, du, dr, entrenador, rival, "Atletismo")
        if validacion == True:
            '''Cada atributo esta escrito de la forma X-D
            con X la primera letra del atributo y D
            una u o r de usuario o rival, esto aplica para cada clase'''
            vu = float(du.velocidad) * p.PONDERADOR_ATLETISMO_VELOCIDAD
            ru = float(du.resistencia) * p.PONDERADOR_ATLETISMO_RESISTENCIA
            mu = float(du.moral) * p.PONDERADOR_ATLETISMO_MORAL

            vr = float(dr.velocidad) * p.PONDERADOR_ATLETISMO_VELOCIDAD
            rr = float(dr.resistencia) * p.PONDERADOR_ATLETISMO_RESISTENCIA
            mr = float(dr.moral) *p.PONDERADOR_ATLETISMO_MORAL

            ptje_usuario = max(p.PUNTAJE_MINIMO, vu + ru + mu)
            ptje_rival = max(p.PUNTAJE_MINIMO, vr + rr + mr)

            if ptje_usuario == ptje_rival:
                return ["Empate", du, dr, "Atletismo"]
            elif ptje_usuario > ptje_rival:
                return ["deportista usuario", du, dr, "Atletismo"]
            else:
                return ["deportista rival", du, dr, "Atletismo"]
        
        else:
            return validacion

class Ciclismo(Deportes):

    def __init__(self):
        super().__init__(True, 0.35, "Ciclismo")

    def validacion_competencia(self, du, dr, entrenador, rival,deporte):
        retorno = Deportes.validacion_competencia(self,du, dr, entrenador, rival, deporte)
        return retorno

    def calcular_ganador(self,du,dr,entrenador, rival):

        du.lesionarse(0.35, entrenador)
        dr.lesionarse(0.35, rival)

        validacion = Atletismo.validacion_competencia(self, du, dr, entrenador, rival, "Ciclismo")
        if validacion == True:
            vu = float(du.velocidad)*p.PONDERADOR_CICLISMO_VELOCIDAD
            ru = float(du.resistencia)*p.PONDERADOR_CICLISMO_RESISTENCIA
            fu = float(du.flexibilidad)*p.PONDERADOR_CICLISMO_FLEXIBIDAD

            vr = float(dr.velocidad)*p.PONDERADOR_CICLISMO_VELOCIDAD
            rr = float(dr.resistencia)*p.PONDERADOR_CICLISMO_RESISTENCIA
            fr = float(dr.flexibilidad)*p.PONDERADOR_CICLISMO_FLEXIBIDAD

            ptje_usuario = max(p.PUNTAJE_MINIMO, vu + ru + fu)
            ptje_rival = max(p.PUNTAJE_MINIMO, vr + rr + fr)


            if ptje_usuario == ptje_rival:
                return ["Empate", du, dr, "Ciclismo"]
            elif ptje_usuario > ptje_rival:
                return ["deportista usuario", du, dr, "Ciclismo"]
            else:
                return ["deportista rival", du, dr, "Ciclismo"]

        else:

            return validacion

class Gimnasia(Deportes):

    def __init__(self):
        super().__init__(True, 0.3, "Gimnasia")

    def validacion_competencia(self, du, dr, entrenador, rival,deporte):
        retorno = Deportes.validacion_competencia(self,du, dr, entrenador, rival, deporte)
        return retorno

    def calcular_ganador(self,du,dr,entrenador, rival):
        du.lesionarse(0.3, entrenador)
        dr.lesionarse(0.3, rival)

        validacion = Atletismo.validacion_competencia(self, du, dr, entrenador, rival, "Gimnasia")
        
        if validacion == True:
            fu = float(du.flexibilidad)*p.PONDERADOR_GIMNASIA_FLEXIBILIDAD
            ru = float(du.resistencia)*p.PONDERADOR_GIMNASIA_RESISTENCIA
            mu = float(du.moral)*p.PONDERADOR_GIMNASIA_MORAL

            fr = float(dr.flexibilidad)*p.PONDERADOR_GIMNASIA_FLEXIBILIDAD
            rr = float(dr.resistencia)*p.PONDERADOR_GIMNASIA_RESISTENCIA
            mr = float(dr.moral)*p.PONDERADOR_GIMNASIA_MORAL

            ptje_usuario = max(p.PUNTAJE_MINIMO, mu + ru + fu)
            ptje_rival = max(p.PUNTAJE_MINIMO, mr + rr + fr)


            if ptje_usuario == ptje_rival:
                return ["Empate", du, dr]
            elif ptje_usuario > ptje_rival:
                return ["deportista usuario", du, dr, "Gimnasia"]
            else:
                return ["deportista rival", du, dr, "Gimnasia"]

        else:
            return validacion


class Natacion(Deportes):

    def __init__(self):
        super().__init__(True, 0.3, "Natacion")

    def validacion_competencia(self, du, dr, entrenador, rival,deporte):
        retorno = Deportes.validacion_competencia(self,du, dr, entrenador, rival, deporte)
        return retorno

    def calcular_ganador(self,du,dr,entrenador, rival):
        du.lesionarse(0.3, entrenador)
        dr.lesionarse(0.3, rival)

        validacion = Atletismo.validacion_competencia(self, du, dr, entrenador, rival, "Natacion")
        if validacion == True:
            fu = float(du.flexibilidad)*p.PONDERADOR_NATACION_FLEXIBILIDAD
            ru = float(du.resistencia)*p.PONDERADOR_NATACION_RESISTENCIA
            vu = float(du.velocidad)*p.PONDERADOR_NATACION_VELOCIDAD

            fr = float(dr.flexibilidad)*p.PONDERADOR_NATACION_FLEXIBILIDAD
            rr = float(dr.resistencia)*p.PONDERADOR_NATACION_RESISTENCIA
            vr = float(dr.velocidad)*p.PONDERADOR_NATACION_VELOCIDAD

            ptje_usuario = max(p.PUNTAJE_MINIMO, vu + ru + fu)
            ptje_rival = max(p.PUNTAJE_MINIMO, vr + rr + fr)

            if ptje_usuario == ptje_rival:
                return ["Empate", du, dr]
            elif ptje_usuario > ptje_rival:
                return ["deportista usuario", du, dr, "Natacion"]
            else:
                return ["deportista rival", du, dr, "Natacion"]
        else:
            return validacion