from random import sample, choice, randint
from time import sleep
from threading import Thread, Event, Lock

from tripulantes import Tripulante, Impostor
from parametros import CANT_TAREAS, CANT_JUGADORES, COLORES_TRIPULANTES
from funciones import cargar_tareas


class DCCrewmates(Thread):

    def __init__(self):
        super().__init__()
        self.impostor = None
        self.tripulantes = []
        self.evento_termino = Event()
        self.evento_sabotaje = Event()
        self.diccionario_tareas = {}

        self.tareas = cargar_tareas()

    def run(self):
        self.asignar_tripulantes()
        self.evento_termino.clear()
        self.impostor.start()
        for tripulant in self.tripulantes:
            tripulant.start()
        for tripulant in self.tripulantes:
            tripulant.join()
        self.evento_termino.set()
        for tarea in self.diccionario_tareas:
            if self.diccionario_tareas[tarea]["realizado"]:
                continue
            else:
                print("Ha ganado el Impostor -_-")
                print("El color del impostor era:",self.impostor.color)
                return
        print("Ha ganado la tripulación!")
        print("El color del impostor era:",self.impostor.color)
        return


    def asignar_tareas(self):
        # Se escoge la cantidad al azar
        tareas_jugador = sample(self.tareas, CANT_TAREAS)

        # Se comprueba que las tareas estén en el diccionario, si no se crea el Lock
        for tarea in tareas_jugador:
            if not self.diccionario_tareas.get(tarea):
                self.diccionario_tareas[tarea] = {
                    "lock": Lock(),
                    "realizado": False,
                    "nombre": tarea,
                }

        # Se retornan las tareas escogidas para un juagdor.
        return tareas_jugador

    def asignar_tripulantes(self):
        colores = COLORES_TRIPULANTES
        # Se escogen los colores de los jugadores al azar
        jugadores = sample(colores, CANT_JUGADORES)

        for color in jugadores[:-1]:
            # Se intancia, se asignan las tareas y se agregan a las lista los tripulantes.
            tareas = self.asignar_tareas()
            tripulante = Tripulante(
                color, tareas, self.evento_sabotaje, self.diccionario_tareas,
            )
            self.tripulantes.append(tripulante)

        # Se crea el impostor.
        self.impostor = Impostor(
            jugadores[-1], [], self.evento_sabotaje, self.diccionario_tareas, 
            self.tripulantes.copy(), self.evento_termino)


if __name__ == '__main__':
    juego = DCCrewmates()
    juego.start()
